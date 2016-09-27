#ifndef _WIN_IOCP_ACCEPTER_H
#define _WIN_IOCP_ACCEPTER_H
#include "win/iocp_worker.h"
#include <vector>
#include <process.h>
namespace netsvc{
	using namespace std;
	template<class handler>
	class iocp_accepter{
	public:
		iocp_accepter();
		~iocp_accepter();

		/*start accepter with listen @port and @worker number, pass @arg to handler's recall method*/
		int start(u_short port, int worker_num, void *arg = NULL);

		/*start accepter with local @ip & listen @port and @worker number, pass @arg to handler's recall method*/
		int start(u_int ip, u_short port, int worker_num, void *arg = NULL);

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

		/*thread function for accept socket from remote*/
		static unsigned __stdcall accept_thread(void *arg);

	private:
		//local bind ip
		UINT _local_ip;
		//listen port
		USHORT _listen_port;
		//listen socket
		SOCKET _listen_sock;

		//max concurrence connections for the accepter
		int _max_conns;
		//max events processed per time for worker
		int _max_events;
		//max wait time for the get iocp status
		int _max_waittm;
		//dispatch strategy
		dispatch_t _dispatch;

		//worker number
		int _worker_num;
		//iocp workers for accepter
		vector<iocp_worker*> _workers;

		//accept thread handler
		HANDLE _hdl;
		//worker thread id
		unsigned _thread_id;
		//stop flag for accepter
		bool _accepter_stop;

		//handler counter
		unsigned _hd_counter;

		//arg pass to every accept connection's handler constructor
		void *_arg;
	};

	template<class handler>
	iocp_accepter<handler>::iocp_accepter():_listen_port(0),_listen_sock(INVALID_SOCKET),_hdl(INVALID_HANDLE_VALUE),_accepter_stop(true),_worker_num(0),_hd_counter(0),_arg(NULL),_max_conns(100000),_max_events(256),_max_waittm(10),_dispatch(round)
	{

	}

	template<class handler>
	iocp_accepter<handler>::~iocp_accepter()
	{

	}

	template<class handler>
	int iocp_accepter<handler>::start(u_short port, int worker_num, void *arg/* = NULL*/)
	{
		return start(INADDR_ANY, port, worker_num, arg);
	}

	template<class handler>
	int iocp_accepter<handler>::start(u_int ip, u_short port, int worker_num, void *arg/* = NULL*/)
	{
		/*initial member*/
		_local_ip = ip;
		_listen_port = port;
		_worker_num = worker_num;
		_arg = arg;

		/*create socket*/
		_listen_sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
		if(_listen_sock == INVALID_SOCKET)
			return -1; //create socket failed

		/*set reuse address*/
		int on = 1;
		if(setsockopt(_listen_sock,SOL_SOCKET,SO_REUSEADDR,(const char*)&on,sizeof(on)) != 0)
			return -1;

		/*bind socket to listen port*/
		struct sockaddr_in addr;
		memset(&addr, 0, sizeof(addr));
		addr.sin_family = AF_INET;
		addr.sin_addr.s_addr = htonl(_local_ip);
		addr.sin_port = htons(_listen_port);
		int err = ::bind(_listen_sock, (struct sockaddr*)&addr, sizeof(addr));
		if(err == SOCKET_ERROR)
			return -1; //bind socket failed.

		/*listen on socket*/
		err = listen(_listen_sock, SOMAXCONN);
		if(err == SOCKET_ERROR)
			return -1; //listen on socket failed.

		/*start iocp workers*/
		int worker_conn_limit = _max_conns/_worker_num;
		for(int i=0; i<_worker_num; i++)
		{
			iocp_worker *worker = new iocp_worker();
			if(worker->start(worker_conn_limit, _max_events, _max_waittm) != 0)
				return -1; 
			_workers.push_back(worker);
		}

		/*start accepter thread*/
		_accepter_stop = false;
		_hdl = (HANDLE)_beginthreadex(NULL, 0, accept_thread, this, 0, &_thread_id);
		if(_hdl == NULL)
		{
			_accepter_stop = true;
			return -1; //start accepter thread failed.
		}

		return 0;
	}

	template<class handler>
	int iocp_accepter<handler>::stop()
	{
		/*stop accept thread first*/
		if(_hdl != INVALID_HANDLE_VALUE)
		{
			_accepter_stop = true;
			WaitForSingleObject(_hdl, INFINITE); //wait for accepter thread to exit
			CloseHandle(_hdl);
		}

		/*stop iocp workers*/
		vector<iocp_worker*>::iterator iter = _workers.begin(), iter_end = _workers.end();
		for(; iter!=iter_end; iter++)
		{
			(*iter)->stop();
			delete *iter;
		}
		_workers.clear();

		/*close socket*/
		closesocket(_listen_sock);

		return 0;
	}

	template<class handler>
	unsigned int iocp_accepter<handler>::concurrency()
	{
		int conn = 0;
		for(int i=0; i<_worker_num; i++)
			conn += _workers[i]->concurrency();
		return conn;
	}

	template<class handler>
	int iocp_accepter<handler>::dispatch(handler *hd)
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
	unsigned iocp_accepter<handler>::accept_thread(void *arg)
	{
		iocp_accepter<handler> *accepter = (iocp_accepter<handler> *)arg;

		while (!accepter->_accepter_stop)
		{
			struct sockaddr_in remote;
			int addr_len = sizeof(remote);
			memset(&remote, 0, addr_len);
			SOCKET s = WSAAccept(accepter->_listen_sock, (struct sockaddr*)&remote, &addr_len, 0, 0);
			if(s != INVALID_SOCKET)
			{
				/*initialize the handler*/
				handler *hd = new handler();
				hd->sock(s);
				hd->peer_ip(ntohl(remote.sin_addr.s_addr));
				hd->peer_port(ntohs(remote.sin_port));
				hd->userarg(accepter->_arg);

				/*dispatch to worker*/
				if(accepter->dispatch(hd) != 0)
					delete hd; //dispatch the handler to a iocp worker
			}
			else
			{
				; //print some error here
			}
		}

		_endthreadex(0);
		return 0;
	}
}
#endif

