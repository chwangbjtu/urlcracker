#include "win/netsvc_util.h"
namespace netsvc{
	SOCKET bind_udp(unsigned int ip, unsigned short port)
	{
		/*create socket*/
		SOCKET sock = socket(AF_INET, SOCK_DGRAM, 0);
		if(sock == INVALID_SOCKET)
			return INVALID_SOCKET;

		/*set reuse address*/
		int on = 1;
		if(setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,(const char*)&on,sizeof(on)) != 0)
		{
			closesocket(sock);
			return INVALID_SOCKET;
		}

		/*bind to local ip & port*/
		SOCKADDR_IN addr;
		memset(&addr, 0, sizeof(addr));
		addr.sin_family = AF_INET;
		addr.sin_addr.s_addr = htonl(ip);
		addr.sin_port = htons(port);
		int err = ::bind(sock, (SOCKADDR*) &addr, sizeof(addr));
		if(err == SOCKET_ERROR)
		{
			closesocket(sock);
			return INVALID_SOCKET; //bind to socket error
		}

		return sock;
	}
}

