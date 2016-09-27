#ifndef _LINUX_UDP_WORKER_H
#define _LINUX_UDP_WORKER_H
#include <list>
#include <pthread.h>
#include "linux/netsvc_util.h"
#include "linux/udp_handler.h"
#include "linux/netsvc_rdwrq.h"

namespace netsvc{
	using namespace std;
	/*
	*	worker class to process the udp packet received by the receiver thread
	*/
	template <class handler>
	class udp_worker
	{
	public:
		udp_worker(void);
		~udp_worker(void);

		/*
		*	start udp worker with local address @ip&port, packet size @psz, queue size @qsz, 
		*condition wait time @qwt in million seconds, @arg what will be passed to the udp 
		*handler object
		*return:
		*	0--success, other--failed.
		*/
		int start(unsigned int ip, unsigned short port, int psz, int qsz, int qwt, void* arg = NULL);

		/*
		*	push a udp packet received by receiver to worker
		*return:
		*	0--success, other--failed.
		*/
		int push(dpacket_t *pkt);
		
		/*
		*	stop udp worker
		*return:
		*	0--success, other--failed.
		*/
		int stop();

	private:
		/*udp process worker thread*/
		static void* worker_thread(void *arg);	

	private:
		//socket used to response
		int _sock;
		//local ip & port
		unsigned int _ip;
		unsigned short _port;

		//packet size from response
		int _packet_sz;
		//queue size for the send & recv queue
		int _queue_sz;
		//waiting time for operate with the recv&send queue
		int _wait_qt;

		//queue for received packet packet
		netsvc_rdwrq _recvq;

		//arg to pass the handler call-back function
		void *_arg;

		//udp handler
		udp_handler *_handler;

		//worker thread handle & id
		pthread_t _thd;
		bool _stop;
	};

	template<class handler>
	udp_worker<handler>::udp_worker():_ip(INADDR_ANY),_port(0),_queue_sz(8192),_wait_qt(100),_arg(NULL),_handler(NULL),_stop(true)
	{

	}

	template<class handler>
	udp_worker<handler>::~udp_worker()
	{

	}

	template<class handler>
	int udp_worker<handler>::start(unsigned int ip, unsigned short port, int psz, int qsz, int qwt, void* arg /* = NULL */)
	{
		/*initialize value*/
		_ip = ip;
		_port = port;
		_arg = arg;
		_packet_sz = psz;
		_queue_sz = qsz;
		_wait_qt = qwt;

		/*create the response socket*/
		_sock = bind_udp(_ip, _port);
		if(_sock == -1)
			return -1;

		/*create the handler object*/
		_handler = new handler();
		_handler->set_socket(_sock);
		_handler->set_ip(_ip);
		_handler->set_port(_port);

		/*initialize recv&send queue*/
		int err = _recvq.init(qsz);
		if(err != 0)
			return -1;

		/*start the worker thread*/
		_stop = false;
		if(pthread_create(&_thd, NULL, worker_thread, this) != 0)
		{
			_stop = true;
			return -1;
		}


		return 0;
	}

	template<class handler>
	int udp_worker<handler>::push(dpacket_t *pkt)
	{
		_recvq.write(pkt);
		return 0;
	}

	template<class handler>
	int udp_worker<handler>::stop()
	{
		/*check if the worker is started*/
		if(_stop)
			return 0;

		/*stop thread*/
		_stop = true;
		pthread_join(_thd, 0);


		return 0;
	}

	template<class handler>
	void* udp_worker<handler>::worker_thread(void *arg)
	{
		udp_worker *pworker = (udp_worker*)arg;
		while(!pworker->_stop)
		{
			void *req_pkt = NULL;
			pworker->_recvq.read(req_pkt);
			if(req_pkt != NULL)
			{
				/*handle the request packet*/
				pworker->_handler->handle((dpacket_t*)req_pkt, pworker->_arg);

				/*free the request packet*/
				delete (dpacket_t*)req_pkt;
			}
		}

		pthread_exit(0);
		return 0;
	}
}
#endif

