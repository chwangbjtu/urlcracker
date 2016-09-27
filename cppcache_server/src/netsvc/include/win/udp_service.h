#ifndef _WIN_UDP_SERVICE_H
#define _WIN_UDP_SERVICE_H
#include <vector>
#include "win/udp_worker.h"
#include "win/udp_receiver.h"

namespace netsvc{
	using namespace std;
	template<class handler>
	class udp_service
	{
		friend class udp_receiver;

	public:
		udp_service();
		virtual ~udp_service();

		/*
		*	start the udp service binding to @port with any local address
		*the @arg will passing the the handler's recall function.
		*return:
		*	0--start service success, other --failed
		*/
		int start(unsigned short port, int worknum, void *arg=NULL);

		/*
		*	start the udp service binding to @port with local @ip
		*the @arg will passing the the handler's recall function.
		*return:
		*	0--start service success, other --failed
		*/
		int start(unsigned int ip, unsigned short port, int worknum, void *arg=NULL);

		/*
		*	stop the udp service
		*/
		int stop();

	public:
		/*adjust the max send & receive queue size for a good performance*/
		void set_max_qsz(int sz){_max_qsz = sz;}
		int get_max_qsz(){return _max_qsz;}

		/*adjust the max send & receive data packet size for application*/
		void set_max_psz(int sz){_max_psz = sz;}
		int get_max_psz(){return _max_psz;}

		/*adjust the wait time for read&write with the read-write queue*/
		void set_wait_qt(int million_sec){_wait_qt = million_sec;}
		int get_wait_qt(){return _wait_qt;}

	private:
		/*push a packet received by the receiver to the workers*/
		void push(dpacket_t *pkt);

	private:
		//local bind ip & port
		unsigned int _ip;
		unsigned short _port;

		//argument for handler recall
		void *_arg;

		//max queue size for send&receiving queue
		int _max_qsz;
		//max packet size for send&receiving in bytes
		int _max_psz;
		//waiting time for read & write a item to read-write queue, in million sec
		int _wait_qt;

		//udp receiver object
		udp_receiver _recver;

		//worker counter
		unsigned int _counter;
		//worker number
		int _worknum;
		//udp worker list
		vector<udp_worker<handler>*> _workers;
	};

	template<class handler>
	udp_service<handler>::udp_service():_ip(INADDR_ANY),_port(0),_counter(0),_worknum(1),_arg(NULL),_max_qsz(8192),_max_psz(1024),_wait_qt(5)
	{
	}

	template<class handler>
	udp_service<handler>::~udp_service()
	{
	}

	template<class handler>
	int udp_service<handler>::start(unsigned short port, int worknum, void *arg/*=NULL*/)
	{
		return start(INADDR_ANY, port, worknum, arg);
	}

	template<class handler>
	int udp_service<handler>::start(unsigned int ip, unsigned short port, int worknum, void *arg/*=NULL*/)
	{
		/*set the parameter*/
		_ip = ip;
		_port = port;
		_worknum = worknum;
		_arg = arg;

		/*start the receiver*/
		int err = _recver.start(_ip, _port, _max_psz, this);
		if(err != 0)
			return -1;

		/*start the workers*/
		for(int i=0; i<_worknum; i++)
		{
			udp_worker<handler> *worker = new udp_worker<handler>();
			err = worker->start(_ip, _port, _max_psz, _max_qsz, _wait_qt, _arg);
			if(err != 0)
				return -1;
			_workers.push_back(worker);
		}

		return 0;
	}

	template<class handler>
	void udp_service<handler>::push(dpacket_t *pkt)
	{
		_workers[_counter++%_worknum]->push(pkt);
	}

	template<class handler>
	int udp_service<handler>::stop()
	{
		/*stop receiver first*/
		_recver.stop();

		/*stop the workers*/
		for(int i=0; i<_worknum; i++)
		{
			_workers[i]->stop();
			delete _workers[i];
		}
		_workers.clear();

		return 0;
	}
}
#endif

