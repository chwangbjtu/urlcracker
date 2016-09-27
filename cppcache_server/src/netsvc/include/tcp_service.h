#ifndef _TCP_SERVICE_H
#define _TCP_SERVICE_H

#if defined(linux) || defined(__linux__) || defined(__linux)
	#include "linux/epoll_handler.h"
	#include "linux/epoll_worker.h"
	#include "linux/epoll_accepter.h"
	#include "linux/epoll_connector.h"
	#define tcp_accepter epoll_accepter
	#define tcp_connector epoll_connector
#elif defined(WIN32)
	#include "win/iocp_handler.h"
	#include "win/iocp_worker.h"
	#include "win/iocp_accepter.h"
	#include "win/iocp_connector.h"
	#define tcp_accepter iocp_accepter
	#define tcp_connector iocp_connector
#else
	#error "netsvc is not supported under this platform!"
#endif

#endif

