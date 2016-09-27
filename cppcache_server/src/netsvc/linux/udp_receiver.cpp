#include "linux/netsvc_type.h"
#include "linux/netsvc_util.h"
#include "linux/udp_service.h"
#include "linux/udp_receiver.h"

namespace netsvc{
	udp_receiver::udp_receiver():_sock(-1),_ip(INADDR_ANY),_port(0),_stop(true),_pktsz(8192),_udpsvc(0)
	{

	}

	udp_receiver::~udp_receiver()
	{

	}

	int udp_receiver::start(unsigned int ip, unsigned short port, int pktsz, void *udpsvc)
	{
		/*set the parameter*/
		_ip = ip;
		_port = port;
		_pktsz = pktsz;
		_udpsvc = udpsvc;

		/*create socket*/
		_sock = bind_udp(_ip, _port);
		if(_sock == -1)
			return -1;

		/*start receive thread*/
		_stop = false;
		if(pthread_create(&_thd, NULL, recv_thread, this) != 0)
		{
			_stop = true;
			return -1;
		}

		return 0;
	}

	int udp_receiver::stop()
	{
		/*check if the receiver is started*/
		if(_stop)
			return 0;

		/*stop thread*/
		_stop = true;
		pthread_join(_thd, 0);

		/*close socket*/
		close(_sock);

		return 0;
	}

	void* udp_receiver::recv_thread(void *arg)
	{
		udp_receiver *precv = (udp_receiver *) arg;
		/*!!recvfrom is blocking, so there is problem with stop action!!*/
		while(!precv->_stop)
		{
			dpacket_t *pkt = new dpacket_t(precv->_pktsz);
			socklen_t addrlen = sizeof(pkt->_addr);
			int sz = recvfrom(precv->_sock, pkt->_buf, pkt->_bsz, 0, (struct sockaddr*)&pkt->_addr, &addrlen);
			if(sz > 0)
			{
				pkt->_dsz = sz;
				((udp_service<udp_handler>*)(precv->_udpsvc))->push(pkt);
			}
			else
			{
				cout<<"fatal error: recvfrom failed."<<endl;
				delete pkt;
				continue;
			}
		}

		pthread_exit(0);
		return 0;
	}
}

