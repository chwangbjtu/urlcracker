#ifndef _WIN_IOCP_CONNECTOR_H
#define _WIN_IOCP_CONNECTOR_H
#include <list>
#include <vector>
#include <process.h>
#include "win/iocp_worker.h"
#include "win/netsvc_rdwrq.h"
using namespace std;

namespace netsvc{
	template<class handler>
	class iocp_connector
	{//an unblocked iocp connector
	public:
		iocp_connector();
		virtual ~iocp_connector();
		/*start connector with @worker number*/
		int start(int worker_num);

		/*connect to remote peer @ip:@port in host byte order with relate arg*/
		int connect(unsigned long ip, unsigned short port, void *arg);

		/*stop connector*/
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
		/*push the pending connecting handler to the pending list*/
		void push(handler *hd);

		/*fetch all the handlers from the pending list*/
		void fetch(list<handler*> &outlst);

		/*dispatch handler @hd with socket @sock to a iocp worker*/
		int dispatch(handler *hd);
		
		/*thread function for nonblocking connect to remote address*/
		static unsigned __stdcall connect_thread(void *arg);

	private:
		//max concurrence connections for the accepter
		int _max_conns;
		//max events processed per time for worker
		int _max_events;
		//max wait time for the get iocp status
		int _max_waittm;
		//dispatch strategy
		dispatch_t _dispatch;

		//connected handler counter
		unsigned int _hd_counter;
		//worker number
		int _worker_num;
		//iocp workers for connector
		vector<iocp_worker*> _workers;

		//mutex for pending connection handlers
		CRITICAL_SECTION _pcrc;
		//pending handlers queue
		list<handler*> _pending_handlers;

		//connect thread handler
		HANDLE _hdl;
		//connect thread id
		unsigned _thread_id;
		//stop flag for connector thread
		bool _connector_stop;
	};
	
	template<class handler>
	iocp_connector<handler>::iocp_connector():_hd_counter(0),_worker_num(0),_hdl(INVALID_HANDLE_VALUE),_connector_stop(true),_max_conns(100000),_max_events(256),_max_waittm(10),_dispatch(round)
	{

	}

	template<class handler>
	iocp_connector<handler>::~iocp_connector()
	{

	}

	template<class handler>
	int iocp_connector<handler>::start(int worker_num)
	{
		/*initial member*/
		_worker_num = worker_num;

		/*initial critical section*/
		InitializeCriticalSection(&_pcrc);

		/*start iocp workers*/
		int worker_conn_limit = _max_conns/_worker_num;
		for(int i=0; i<_worker_num; i++)
		{
			iocp_worker *worker = new iocp_worker();
			if(worker->start(worker_conn_limit, _max_events, _max_waittm) != 0)
				return -1; 
			_workers.push_back(worker);
		}

		/*start connector thread*/
		_connector_stop = false;
		_hdl = (HANDLE)_beginthreadex(NULL, 0, connect_thread, this, 0, &_thread_id);
		if(_hdl == NULL)
		{
			_connector_stop = true;
			return -1; //start accepter thread failed.
		}

		return 0;
	}

	template<class handler>
	int iocp_connector<handler>::connect(unsigned long ip, unsigned short port, void *arg)
	{
		/*create socket*/
		SOCKET sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, WSA_FLAG_OVERLAPPED);
		if(sock == INVALID_SOCKET)
			return -1; //create socket failed

		/*set socket to nonblock mode*/
		unsigned long io_mode = 1;
		int err = ioctlsocket(sock, FIONBIO, &io_mode);
		if(err != 0)
		{
			closesocket(sock);
			return -1;
		}

		/*bind remote address*/
		struct sockaddr_in addr;
		memset(&addr, 0, sizeof(addr));
		addr.sin_family = AF_INET;
		addr.sin_addr.s_addr = htonl(ip);
		addr.sin_port = htons(port);

		/*connect to remote*/
		err = WSAConnect(sock, (struct sockaddr*)&addr, sizeof(addr), NULL, NULL, NULL, NULL);
		if(err != 0)
		{
			int eno = WSAGetLastError();
			if(eno != WSAEWOULDBLOCK)
			{
				closesocket(sock);
				return -1;
			}
		}

		/*set the address information to handler*/
		handler *hdr = new handler();
		hdr->userarg(arg);
		hdr->sock(sock);
		hdr->peer_ip(ip);
		hdr->peer_port(port);

		/*push the handler to pending list*/
		push(hdr);

		return 0;
	}

	template<class handler>
	int iocp_connector<handler>::stop()
	{
		/*stop connector thread*/
		if(!_connector_stop)
		{
			_connector_stop = true;
			WaitForSingleObject(_hdl, INFINITE); //wait for accepter thread to exit
			CloseHandle(_hdl);
		}

		/*free the pending connect handlers*/
		EnterCriticalSection(&_pcrc);
		list<handler*>::iterator piter = _pending_handlers.begin(), piter_end = _pending_handlers.end();
		for(; piter!=piter_end; piter++)
		{
			((*piter))->on_close();
			delete *piter;
		}
		_pending_handlers.clear();
		LeaveCriticalSection(&_pcrc);

		/*stop iocp workers*/
		vector<iocp_worker*>::iterator iter = _workers.begin(), iter_end = _workers.end();
		for(; iter!=iter_end; iter++)
		{
			(*iter)->stop();
			delete *iter;
		}
		_workers.clear();

		/*delete critical section*/
		DeleteCriticalSection(&_pcrc);

		return 0;
	}

	template<class handler>
	unsigned int iocp_connector<handler>::concurrency()
	{
		int conn = 0;
		for(int i=0; i<_worker_num; i++)
			conn += _workers[i]->concurrency();
		return conn;
	}

	template<class handler>
	void iocp_connector<handler>::push(handler *hd)
	{
		EnterCriticalSection(&_pcrc);
		_pending_handlers.push_back(hd);
		LeaveCriticalSection(&_pcrc);
	}

	template<class handler>
	void iocp_connector<handler>::fetch(list<handler*> &outlst)
	{
		EnterCriticalSection(&_pcrc);
		outlst.splice(outlst.end(), _pending_handlers);
		LeaveCriticalSection(&_pcrc);
	}

	template<class handler>
	int iocp_connector<handler>::dispatch(handler *hd)
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
	unsigned iocp_connector<handler>::connect_thread(void *arg)
	{
		/*pending handlers wait for connect result*/
		list<handler*> hds;

		iocp_connector *connector = (iocp_connector *)arg;
		while (!connector->_connector_stop)
		{
			/*fetch the pending handlers*/
			connector->fetch(hds);

			/*check each pending handlers*/
			if(!hds.empty())
			{
				list<handler*>::iterator iter=hds.begin(), iter_end=hds.end();
				while(iter != iter_end)
				{	
					/*get the handler*/
					handler *hd = *iter;
					SOCKET sock = hd->sock();

					/*bind to fd sets*/
					fd_set writefds;
					FD_ZERO(&writefds);
					fd_set exptfds;
					FD_ZERO(&exptfds);
					FD_SET(sock, &writefds);
					FD_SET(sock, &exptfds);

					/*not wait when select*/
					struct timeval tv;
					tv.tv_sec = 0;
					tv.tv_usec = 0;

					/*process the select operation*/
					int fds = select(0, NULL, &writefds, &exptfds, &tv);
					if(fds > 0)
					{
						if (!FD_ISSET(sock, &writefds) || connector->dispatch(hd) != 0)
						{
							/*first invoke the on open method, pass the arg to handler object*/
							hd->on_open(hd->userarg());
							/*then invoke the close method, for the user to do something*/
							hd->on_close();
							/*free the handler object*/
							delete hd;
						}

						hds.erase(iter++);
					}
					else if(fds<0)
					{
						/*first invoke the on open method, pass the arg to handler object*/
						hd->on_open(hd->userarg());
						/*then invoke the close method, for the user to do something*/
						hd->on_close();
						/*free the handler object*/
						delete hd;

						hds.erase(iter++);
					}
					else
					{//no operation ready on the socket, check the next one
						iter++;
					}
				}
			}
			else
			{/*sleep for 10ms*/
				Sleep(10);
			}
		}
		_endthreadex(0);
		return 0;
	}
}
#endif

