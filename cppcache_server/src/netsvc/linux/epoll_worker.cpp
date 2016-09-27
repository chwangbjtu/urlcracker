#include "linux/epoll_worker.h"

namespace netsvc{
	epoll_worker::epoll_worker():_epoll_fd(-1),_worker_stop(true),_max_conns(100000),_max_events(256),_max_waittm(10),_concurrency(0)
	{
	}

	epoll_worker::~epoll_worker(void)
	{
	}

	int epoll_worker::start(int maxconns, int maxevents, int maxwaitm,int thread_index)
	{
		/*set the parameters*/
		_max_conns = maxconns;
		_max_events = maxevents;
		_max_waittm = maxwaitm;
        _thread_index = thread_index;

		/*initial pending connection queue*/
		int err = _pendq.init(8192);
		if(err != 0)
			return -1;

		/*create epoll*/
		_epoll_fd = epoll_create(256);
		if(_epoll_fd == -1)
			return -1;

		/*start worker thread*/
		_worker_stop = false;
		if(pthread_create(&_thread_worker, NULL, work_thread, this) != 0)
		{
			_worker_stop = true;
			return -1;
		}

		return 0;
	}

	int epoll_worker::stop()
	{
		/*stop worker thread*/
		_worker_stop = true;
		pthread_join(_thread_worker, 0);

		/*close the epoll*/
		if(_epoll_fd != 0)
			close(_epoll_fd);
		_epoll_fd = -1;

		return 0;
	}

	unsigned int epoll_worker::concurrency()
	{
		return _concurrency + _pendq.size();	
	}

	void epoll_worker::reset_concurrency()
	{
		_concurrency = _handlers.size();
	}

    int epoll_worker::thread_index()
    {
        return _thread_index;
    }

	int epoll_worker::dispatch(epoll_handler *hd)
	{
		int err = _pendq._write(hd);
		if(err != 0)
			return -1;
		return 0;
	}

	int epoll_worker::accept(int thread_index)
	{
		void *hdptr = NULL;
		int err = _pendq._read(hdptr);
		while(err == 0)
		{
			epoll_handler *hd = (epoll_handler*)hdptr;
			int sock = hd->sock();
			
			if(_handlers.size() < _max_conns)
			{
				if(hd->handle_open(hd->userarg()) != 0)
				{
					hd->handle_close();
					delete hd;
				}
				else
				{
                    hd->thread_index(thread_index);
					int epoll_opt = EPOLL_CTL_ADD;
					u_int events = EPOLLERR|EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET;

					struct epoll_event ev;
					ev.events = events;
					ev.data.ptr = hd;

					if(epoll_ctl(_epoll_fd, epoll_opt, sock, &ev) == -1)
					{
						hd->handle_error(errno);
						hd->handle_close();
						delete hd;
					}
					else
						_handlers.insert(pair<int, epoll_handler*>(sock, hd));
				}
			}
			else
			{
				delete hd;
			}

			err = _pendq._read(hdptr);
		}

		return 0;
	}

	void epoll_worker::run_handlers()
	{
		/*get the run time*/
		time_t tm = time(NULL);

		/*run all handlers*/
		map<int, epoll_handler*>::iterator iter=_handlers.begin(), iter_end=_handlers.end();
		while(iter!=iter_end)
		{
			/*check the timer of each handler first*/
			if(iter->second->is_timeout(tm))
			{
				int err = iter->second->handle_timeout();
				if(err != 0)
				{
					iter->second->handle_close();
					delete iter->second;
					_handlers.erase(iter++);
					continue;
				}
			}


			/*recall the handler run of each handler*/
			int err = iter->second->handle_run(tm);
			if(err != 0)
			{
				iter->second->handle_close();
				delete iter->second;
				_handlers.erase(iter++);
			}
			else
				iter++;
		}
	}

	void epoll_worker::free_handlers()
	{
		map<int, epoll_handler*>::iterator iter=_handlers.begin(), iter_end=_handlers.end();
		for(; iter!=iter_end; iter++)
		{
			iter->second->handle_close();
			delete iter->second;
		}
		_handlers.clear();

		void *hdptr = NULL;
		int err = _pendq.read(hdptr, _max_waittm);
		while(err == 0)
		{
			epoll_handler *hd = (epoll_handler*)hdptr;
			hd->handle_open(hd->userarg());
			hd->handle_close();
			delete hd;

			err = _pendq.read(hdptr, _max_waittm);
		}
	}

	int epoll_worker::remove(int sock)
	{
		int ret = 0;

		map<int, epoll_handler*>::iterator iter = _handlers.find(sock);
		if(iter != _handlers.end())
		{
			iter->second->handle_close();
			delete iter->second;
			_handlers.erase(iter);
		}
		else
			ret = -1;

		return ret;
	}

	void* epoll_worker::work_thread(void *arg)
	{
		epoll_worker* worker = (epoll_worker*) arg;
		int max_events = worker->_max_events;
		int max_waittm = worker->_max_waittm;
        int thread_index = worker->_thread_index;
		struct epoll_event *events = new epoll_event[max_events];

		while(!worker->_worker_stop)
		{
			/*accept the new handlers in the pending map*/
			worker->accept(thread_index);

			/*process the handlers in the epoll*/
			int num = epoll_wait(worker->_epoll_fd, events, max_events, max_waittm);
			for(int i=0; i<num; i++)
			{
				int err = 0;
				epoll_handler *hd = (epoll_handler*)events[i].data.ptr;

				if(err == 0 && events[i].events & EPOLLIN)
					err |= hd->handle_recv();

				if(err == 0 && (events[i].events & EPOLLOUT))
					err |= hd->handle_send();

				if(err == 0 && (events[i].events & EPOLLRDHUP))
					err |= hd->handle_shutd();

				if(err == 0 && (events[i].events & EPOLLERR))
					err |= hd->handle_error(errno);

				if(err != 0)
					worker->remove(hd->sock());
			}

			/*give cpu resource to every handlers in the epoll*/
			worker->run_handlers();

			/*reset the concurrency*/
			worker->reset_concurrency();
		}
		
		delete []events;

		worker->free_handlers();

		pthread_exit(0);
		return 0;
	}
}
