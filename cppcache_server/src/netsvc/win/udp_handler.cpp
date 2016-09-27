#include "win/udp_handler.h"

namespace netsvc{
	udp_handler::udp_handler(void):_sock(INVALID_SOCKET),_ip(0),_port(0)
	{
	}

	udp_handler::~udp_handler(void)
	{
	}

	int udp_handler::sendto(const struct sockaddr *to, const char *resp, int sz)
	{
		int snd = ::sendto(_sock, resp, sz, 0, to, sizeof(struct sockaddr));
		if(snd == SOCKET_ERROR)
			return -1;
		return 0;
	}
}

