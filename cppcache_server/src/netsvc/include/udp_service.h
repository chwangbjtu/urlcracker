#ifndef _UDP_SERVICE_H
#define _UDP_SERVICE_H

#if defined(linux) || defined(__linux__) || defined(__linux)
	#include "linux/udp_handler.h"
	#include "linux/udp_worker.h"
	#include "linux/udp_receiver.h"
	#include "linux/udp_service.h"
#elif defined(WIN32)
	#include "win/udp_handler.h"
	#include "win/udp_worker.h"
	#include "win/udp_receiver.h"
	#include "win/udp_service.h"
#else
	#error "netsvc is not supported under this platform!"
#endif

#endif


