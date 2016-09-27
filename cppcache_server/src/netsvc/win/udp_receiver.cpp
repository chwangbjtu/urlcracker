#include "win/netsvc_type.h"
#include "win/netsvc_util.h"
#include "win/udp_service.h"
#include "win/udp_receiver.h"

namespace netsvc{
	udp_receiver::udp_receiver():_sock(INVALID_SOCKET),_ip(INADDR_ANY),_port(0),_recv_thd(INVALID_HANDLE_VALUE),_recv_thd_id((unsigned)-1),_recv_thd_stop(true),_pktsz(8192),_udpsvc(0)
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
		if(_sock == INVALID_SOCKET)
			return -1;

		/*start receive thread*/
		_recv_thd_stop = false;
		_recv_thd = (HANDLE)_beginthreadex(NULL, 0, recv_thread, this, 0, &_recv_thd_id);
		if(_recv_thd == NULL)
		{
			_recv_thd_stop = true;
			return -1;
		}

		return 0;
	}

	int udp_receiver::stop()
	{
		/*check if the worker is started*/
		if(_recv_thd_stop)
			return 0;

		/*stop thread*/
		_recv_thd_stop = true;
		WaitForSingleObject(_recv_thd, INFINITE);
		CloseHandle(_recv_thd);

		/*close socket*/
		closesocket(_sock);

		return 0;
	}

	unsigned udp_receiver::recv_thread(void *arg)
	{
		udp_receiver *precv = (udp_receiver *) arg;
		/*!!recvfrom is blocking, so there is problem with stop action!!*/
		while(!precv->_recv_thd_stop)
		{
			dpacket_t *pkt = new dpacket_t(precv->_pktsz);
			int addrlen = sizeof(pkt->_addr);
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

		_endthreadex(0);
		return 0;
	}
}

