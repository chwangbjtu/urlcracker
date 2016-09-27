#ifndef _WIN_NETSVC_UTIL_H
#define _WIN_NETSVC_UTIL_H
#include <WinSock2.h>

namespace netsvc{
	/*
	*	return a udp socket bind with @ip & @port
	*/
	extern SOCKET bind_udp(unsigned int ip, unsigned short port);
}
#endif

