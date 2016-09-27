#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include "linux/netsvc_util.h"

namespace netsvc{
	int bind_udp(unsigned int ip, unsigned short port)
	{
		/*create socket*/
		int sock = socket(AF_INET, SOCK_DGRAM, 0);
		if(sock == -1)
			return -1; //create socket failed

		/*set reuse address*/
		int on = 1;
		if(setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,&on,sizeof(on)) != 0)
			return -1;

		/*bind to port*/
		struct sockaddr_in addr;
		memset(&addr, 0, sizeof(addr));
		addr.sin_family = AF_INET;
		addr.sin_addr.s_addr = htonl(ip);
		addr.sin_port = htons(port);
		int err = ::bind(sock, (struct sockaddr*) &addr, sizeof(addr));
		if(err != 0)
			return -1; //bind to socket error

		return sock;
	}
}

