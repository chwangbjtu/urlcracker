#ifndef _LINUX_EPOLL_ACCEPTER_H
#define _LINUX_EPOLL_ACCEPTER_H
#include <string.h>
#include <vector>
#include <pthread.h>
#include <unistd.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "linux/epoll_worker.h"
namespace netsvc{
	using namespace std;
	/*epoll accepter service using EDGE trigger*/
	template<class handler>
	class epoll_accepter{
	public:
		epoll_accepter();
		~epoll_accepter();

		/*start accepter with listen @port and @worker number with edge trigger, @arg will be passed to handler*/
		int start(unsigned short port, int worker_num, void *arg = NULL);

		/*start accepter with local @ip & listen @port and @worker number with edge trigger, @arg will be passed to handler*/
		int start(unsigned int ip, unsigned short port, int worker_num, void *arg = NULL);

		/*stop accepter*/
		int stop();

		/*concurrent connection status*/
		unsigned int concurrency();

	public:
		/*set&get the max connections concurrence limit*/
		void set_max_conns(int maxconns){_max_conns = maxconns;}
		int get_max_conns(){return _max_conns;}

		/*set&get the max events processed for each iocp worker*/
		void set_max_events(int maxevt){_max_events = maxevt;}
		int get_max_events(){return _max_events;}

		/*set&get the max wait time for wait an iocp event, in million seconds*/
		void set_max_waittm(int maxwt){_max_waittm = maxwt;}
		int get_max_waittm(){return _max_waittm;}

		/*set&get the dispatch strategy of new connection to workers*/
		void set_dispatch(dispatch_t type){_dispatch = type;}
		dispatch_t get_dispatch(){return _dispatch;}

	private:
		/*dispatch handler @hd with socket @s to a iocp worker*/
		int dispatch(handler *hd);

		/*make the @fd nonblock mode*/
		static int set_nonblock(int fd);

		/*thread function for accept socket from remote*/
		static void * accept_thread(void *arg);

	private:
		//local bind ip
		unsigned int _local_ip;
		//listen port
		unsigned short _listen_port;
		//listen socket
		int _listen_sock;

		//max concurrence connections for the accepter
		int _max_conns;
		//max events processed per time for worker
		int _max_events;
		//max wait time for the get iocp status
		int _max_waittm;
		//dispatch strategy
		dispatch_t _dispatch;

		//handler counter
		unsigned int _hd_counter;
		//worker number
		int _worker_num;
		//iocp workers for accepter
		vector<epoll_worker*> _workers;

		//accept thread handler
		pthread_t _thread_accepter;
		//stop flag for accepter
		bool _accepter_stop;

		//arg pass to every accept connection's handler constructor
		void *_arg;
	};

	template<class handler>
	epoll_accepter<handler>::epoll_accepter():_listen_port(0),_listen_sock(-1),_accepter_stop(true),_worker_num(0),_hd_counter(0),_arg(NULL),_max_conns(100000),_max_events(256),_max_waittm(10),_dispatch(round)
	{

	}

	template<class handler>
	epoll_accepter<handler>::~epoll_accepter()
	{

	}

	template<class handler>
	int epoll_accepter<handler>::start(unsigned short port, int worker_num, void *arg /* = NULL */)
	{
		return start(INADDR_ANY, port, worker_num, arg);
	}

	template<class handler>
	int epoll_accepter<handler>::start(unsigned int ip, unsigned short port, int worker_num, void *arg/*=NULL*/)
	{
		if(worker_num <=0 )
			return -1;

		/*initial member*/
		_local_ip = ip;
		_listen_port = port;
		_worker_num = worker_num;
		_arg = arg;

		/*create socket*/
		_listen_sock = socket(AF_INET, SOCK_STREAM, 0);
		if(_listen_sock == -1)
			return -1; //initial socket error

		/*set reuse address*/
		int on = 1;
		if(setsockopt(_listen_sock,SOL_SOCKET,SO_REUSEADDR,&on,sizeof(on)) != 0)
			return -1;

		/*set local address*/
		struct sockaddr_in addr;
		memset(&addr, 0, sizeof(addr));
		addr.sin_family = AF_INET;
		addr.sin_port = htons(_listen_port);
		addr.sin_addr.s_addr = htonl(ip);

		/*bind socket to local address*/
		if(::bind(_listen_sock, (struct sockaddr *)&addr, sizeof(addr)) != 0)
			return -1;

		/*start listening*/
		if(listen(_listen_sock, SOMAXCONN) != 0)
			return -1;

		/*start epoll io workers*/
		int worker_conn_limit = _max_conns/_worker_num;
		for(int i=0; i<_worker_num; i++)
		{
			epoll_worker *worker = new epoll_worker();
			if(worker->start(worker_conn_limit, _max_events, _max_waittm,i) != 0)
				return -1;
			_workers.push_back(worker);
		}

		/*start the accept thread*/
		_accepter_stop = false;
		if(pthread_create(&_thread_accepter, NULL, accept_thread, this) != 0)
		{
			_accepter_stop = true;
			return -1;
		}

		return 0;
	}

	template<class handler>
	int epoll_accepter<handler>::stop()
	{
		/*stop accept thread first*/
		_accepter_stop = true;
		pthread_join(_thread_accepter, 0);

		/*stop epoll workers*/
		vector<epoll_worker*>::iterator iter = _workers.begin(), iter_end = _workers.end();
		for(; iter!=iter_end; iter++)
		{
			(*iter)->stop();
			delete *iter;
		}
		_workers.clear();

		/*close socket*/
		close(_listen_sock);

		return 0;
	}

	template<class handler>
	unsigned int epoll_accepter<handler>::concurrency()
	{
		unsigned int conn = 0;
		for(int i=0; i<_worker_num; i++)
			conn += _workers[i]->concurrency();
		return conn;
	}

	template<class handler>
	int epoll_accepter<handler>::dispatch(handler *hd)
	{
		if(_dispatch == round)
		{
			int err = _workers[_hd_counter++%_worker_num]->dispatch(hd);
			if(err != 0)
				return -1;
		}
		else
		{
			int pos = 0;
			unsigned int minload = (unsigned int)-1;

			for(int i=0; i<_worker_num; i++)
			{
				unsigned int load = _workers[i]->concurrency();
				if(load < minload)
				{
					minload = load;
					pos = i;
				}
			}

			int err = _workers[pos]->dispatch(hd);
			if(err != 0)
				return -1;
		}

		return 0;
	}

	template<class handler>
	int epoll_accepter<handler>::set_nonblock(int fd)
	{
		int opts = fcntl(fd, F_GETFL);
		if(opts < 0) 
			return -1;
		opts = opts | O_NONBLOCK;
		if(fcntl(fd, F_SETFL, opts) < 0)
			return -1;
		return 0;
	}

	template<class handler>
	void* epoll_accepter<handler>::accept_thread(void *arg)
	{
		epoll_accepter<handler> *accepter = (epoll_accepter<handler> *)arg;

		while (!accepter->_accepter_stop)
		{
			struct sockaddr_in remote_addr;
			socklen_t addr_len = sizeof(remote_addr);
			memset(&remote_addr, 0, addr_len);
			int sock = accept(accepter->_listen_sock, (struct sockaddr*)&remote_addr, &addr_len);
			if(sock >= 0)
			{//new connection
				if(set_nonblock(sock) != 0)
				{//set nonblock for the socket, if failed, close it and continue
					close(sock);
					continue;
				}

				handler *hd = new handler();
				hd->sock(sock);
				hd->peer_ip(ntohl(remote_addr.sin_addr.s_addr));
				hd->peer_port(ntohs(remote_addr.sin_port));
				hd->userarg(accepter->_arg);

				if(accepter->dispatch(hd) != 0)
					delete hd;
			}
			else
			{
				;//print error, should nerve happened
			}
		}

		pthread_exit(0);
		return 0;
	}
}
#endif

