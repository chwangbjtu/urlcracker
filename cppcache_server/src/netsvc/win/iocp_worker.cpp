#include "win/iocp_worker.h"
#include <time.h>
#include <process.h>
namespace netsvc{
	iocp_worker::iocp_worker(void):_worker_stop(true),_max_conns(100000),_max_events(256),_max_waittm(10),_concurrency(0)
	{
	}

	iocp_worker::~iocp_worker(void)
	{
	}

	int iocp_worker::start(int maxconns, int maxevents, int maxwaitm)
	{
		/*set the parameters*/
		_max_conns = maxconns;
		_max_events = maxevents;
		_max_waittm = maxwaitm;

		/*initial pending connection queue*/
		int err = _pendq.init(8192);
		if(err != 0)
			return -1;

		/*create io complete port*/
		_iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, 0);
		if(_iocp == NULL)
			return -1; //create iocp failed.

		/*start worker thread*/
		_worker_stop = false;
		_hdl = (HANDLE)_beginthreadex(NULL, 0, work_thread, this, 0, &_thread_id);
		if(_hdl == NULL)
		{
			_worker_stop = true;
			return -1; //start worker thread failed.
		}

		return 0;
	}

	int iocp_worker::stop()
	{
		/*stop worker thread*/
		_worker_stop = true;
		WaitForSingleObject(_hdl, INFINITE);

		/*close the iocp*/
		CloseHandle(_iocp);

		return 0;
	}

	unsigned int iocp_worker::concurrency()
	{
		return _concurrency + _pendq.size();	
	}

	int iocp_worker::dispatch(iocp_handler *hd)
	{
		int err = _pendq._write(hd);
		if(err != 0)
			return -1;
		return 0;
	}

	int iocp_worker::accept()
	{
		void *hdptr = NULL;
		int err = _pendq._read(hdptr);

		while(err == 0)
		{
			iocp_handler *hd = (iocp_handler *)hdptr;
			SOCKET s = hd->sock();
			
			if((int)_handlers.size() < _max_conns)
			{
				/*add the new handler to the iocp*/
				if(CreateIoCompletionPort((HANDLE)s, _iocp, (ULONG_PTR)hd, 0) != NULL)
				{
					/*invoke the on open method of handler*/
					int err = hd->on_open(hd->userarg());
					if(err != 0)
					{
						hd->on_close();
						delete hd;
					}
					else
						_handlers.insert(pair<SOCKET, iocp_handler*>(s, hd));
				}
				else
				{
					delete hd;
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

	void iocp_worker::run_handlers()
	{
		time_t tm = time(NULL);
		map<SOCKET, iocp_handler*>::iterator iter=_handlers.begin(), iter_end=_handlers.end();
		while(iter!=iter_end)
		{
			/*check the timer of each handler first*/
			if(iter->second->is_timeout(tm))
			{
				int err = iter->second->on_timeout();
				if(err != 0)
				{
					iter->second->on_close();
					delete iter->second;
					_handlers.erase(iter++);
					continue;
				}
			}

			/*recall the handler run of each handler*/
			int err = iter->second->on_running(tm);
			if(err != 0)
			{
				iter->second->on_close();
				delete iter->second;
				_handlers.erase(iter++);
			}
			else
				iter++;
		}
	}

	void iocp_worker::free_handlers()
	{
		/*free all handlers*/
		map<SOCKET, iocp_handler*>::iterator iter=_handlers.begin(), iter_end=_handlers.end();
		iter=_handlers.begin();
		for(; iter!=iter_end; iter++)
		{
			iter->second->on_close();
			delete iter->second;
		}
		_handlers.clear();

		void *hdptr = NULL;
		int err = _pendq.read(hdptr, _max_waittm);

		while(err == 0)
		{
			iocp_handler *hd = (iocp_handler *)hdptr;
			hd->on_close();
			delete hd;
			err = _pendq.read(hdptr, _max_waittm);
		}
	}

	int iocp_worker::remove(SOCKET s)
	{
		int ret = 0;

		map<SOCKET, iocp_handler*>::iterator iter = _handlers.find(s);
		if(iter != _handlers.end())
		{
			iter->second->on_close();
			delete iter->second;
			_handlers.erase(iter);
		}
		else
			ret = -1;

		return ret;
	}

	iocp_handler* iocp_worker::handler(SOCKET s)
	{
		iocp_handler *hd = NULL;

		map<SOCKET, iocp_handler*>::iterator iter = _handlers.find(s);
		if(iter != _handlers.end())
			hd = iter->second;

		return hd;
	}

	void iocp_worker::reset_concurrency()
	{
		_concurrency = _handlers.size();
	}

	unsigned iocp_worker::work_thread(void *arg)
	{
		iocp_worker* worker = (iocp_worker*) arg;
		while(!worker->_worker_stop)
		{
			iocp_overlapped *olp = NULL;
			DWORD transfered = 0;
			iocp_handler *hd = NULL;
			int counter = 0;

			while(counter++ < worker->_max_events)
			{
				/*accept the new connection*/
				worker->accept();

				/*process the handlers in the iocp*/
				BOOL bok = GetQueuedCompletionStatus(worker->_iocp, &transfered, (PULONG_PTR)&hd, (LPOVERLAPPED*)&olp, worker->_max_waittm);
				if(bok)
				{
					iocp_handler *hd1 = worker->handler(olp->_sock);
					if(hd1 == hd)
					{
						if(transfered == 0)
						{//socket closed
							worker->remove(olp->_sock);
							delete olp;
						}
						else
						{
							int err = 0;
							if(olp->_opt == IOCP_SEND)
							{
								err = hd->on_send(transfered);
							}
							else if(olp->_opt == IOCP_RECV)
							{
								err = hd->on_recv(olp->_buf.buf, transfered);
							}
							else
							{//IOCP_ERR, should never happened!
								err = hd->on_error(WSAGetLastError());
							}

							if(err != 0)
								worker->remove(olp->_sock);

							delete olp;
						}
					}
					else
					{//only free olp, handler has freed already
						delete olp;
					}
				}
				else
				{
					int err = WSAGetLastError();
					if(err != WSA_WAIT_TIMEOUT)
					{
						worker->remove(olp->_sock);
						delete olp;
					}
					else
						break;
				}
			}

			//running all handlers
			worker->run_handlers();

			//reset the concurrency
			worker->reset_concurrency();
		}

		worker->free_handlers();

		_endthreadex(0);
		return 0;
	}
}