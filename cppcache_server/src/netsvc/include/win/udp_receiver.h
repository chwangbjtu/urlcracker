#ifndef _WIN_UDP_RECEIVER_H
#define _WIN_UDP_RECEIVER_H
#include <vector>
#include <iostream>
#include <process.h>
#include <WinSock2.h>

namespace netsvc{
	using namespace std;
	class udp_receiver{
	public:
		udp_receiver();
		~udp_receiver();

		/*
		*	start the udp receiver service on @port with local address @ip.
		*the max received packet size is @pktsz. and the service object @udpsvc
		*return:
		*	0--start service success, other --failed
		*/
		int start(unsigned int ip, unsigned short port, int pktsz, void *udpsvc);

		/*
		*	stop the udp receiver service
		*/
		int stop();

	private:
		/*
		*	udp receive thread of accepter
		*/
		static unsigned __stdcall recv_thread(void *arg);

	private:
		//udp socket relate with the @_port
		SOCKET _sock;
		//local bind ip address
		unsigned int _ip;
		//udp port for receive data
		unsigned short _port;

		//receive thread handle & id
		HANDLE _recv_thd;
		unsigned _recv_thd_id;
		bool _recv_thd_stop;

		//receive packet size
		int _pktsz;
		//pointer to the udp service object
		void *_udpsvc;
	};
}
#endif

