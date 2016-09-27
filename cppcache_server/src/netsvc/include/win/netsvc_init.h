#ifndef _WIN_NETSVC_INIT_H
#define _WIN_NETSVC_INIT_H
#include <iostream>
#include <WinSock2.h>

class netsvc_init
{
public:
	netsvc_init()
	{
		/*start up windows socket environment*/
		WORD wsaversion;
		WSADATA wsadata;
		wsaversion = MAKEWORD( 2, 2 );

		int err = WSAStartup(wsaversion, &wsadata);
		if ( err != 0 ) 
		{ //startup windows socket environment failed.
			std::cerr<<"windows socket startup failed, error: "<<WSAGetLastError()<<std::endl;
			exit(1);
		}
	}

	~netsvc_init()
	{
		/*clean the windows socket environment*/
		WSACleanup();
	}
};

//for initialize the windows socket environment
static netsvc_init _g_netsvc_init;
#endif