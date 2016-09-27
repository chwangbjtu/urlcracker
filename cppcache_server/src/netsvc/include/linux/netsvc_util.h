#ifndef _LINUX_NETSVC_UTIL_H
#define _LINUX_NETSVC_UTIL_H
namespace netsvc{
	/*
	*	return a udp socket bind with @ip & @port
	*/
	extern int bind_udp(unsigned int ip, unsigned short port);
}
#endif

