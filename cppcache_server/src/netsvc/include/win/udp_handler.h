#ifndef _WIN_UDP_HANDLER_H
#define _WIN_UDP_HANDLER_H
#include <WinSock2.h>
#include "win/netsvc_type.h"
#include "win/netsvc_rdwrq.h"

namespace netsvc{
	/*
	*	base class of the udp service handler, must be realized when 
	*using the udp service module.
	*/
	class udp_handler
	{
	public:
		udp_handler(void);
		virtual ~udp_handler(void);

	public:
		/*set the local service information*/
		inline void set_socket(SOCKET sock){_sock = sock;}
		inline void set_ip(unsigned int ip){_ip = ip;}
		inline void set_port(unsigned short port){_port = port;}

		inline SOCKET get_socket(){return _sock;}
		inline unsigned int get_ip(){return _ip;}
		inline unsigned short get_port(){return _port;} 

	public:
		/*
		*	handle udp request with request package object @req, if need response please call the
		*@sendto method. @arg is the input the the udp service when startup.
		*return:
		*	0--handle success, <0--something error happened.
		*/
		virtual int handle(dpacket_t *req, void *arg=NULL) = 0;

	protected:
		/*
		*	send response packet to the peer. first make a @dpacket_t object for the
		*response data @resp with size @sz, and push it to the send queue.
		*return:
		*	0--send success, <0--something error happened.
		*/
		int sendto(const struct sockaddr *to, const char *resp, int sz);

	private:
		/*local udp service information*/
		//local socket
		SOCKET _sock;
		//local ip
		unsigned int _ip;
		//local port
		unsigned short _port;
	};
}
#endif

