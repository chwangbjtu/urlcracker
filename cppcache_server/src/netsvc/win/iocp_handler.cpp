#include "win/iocp_handler.h"

namespace netsvc{
	iocp_handler::iocp_handler():_sock(INVALID_SOCKET),_ip(0),_port(0),_timer_tm((time_t)(-1)),_userarg(NULL)
	{

	}

	iocp_handler::~iocp_handler(void)
	{
		if(_sock != INVALID_SOCKET)
			closesocket(_sock);
		_sock = INVALID_SOCKET;
	}

	int iocp_handler::on_open(void *arg)
	{
		return -1;
	}

	int iocp_handler::on_send(int sz_send)
	{
		return -1;
	}

	int iocp_handler::on_recv(const char*data, int sz_recv)
	{
		return -1;
	}

	int iocp_handler::on_close()
	{
		return -1;
	}

	int iocp_handler::on_error(int err)
	{
		return -1;
	}

	int iocp_handler::on_timeout()
	{
		return -1;
	}

	int iocp_handler::on_running(time_t tm)
	{
		return -1;
	}

	int iocp_handler::async_send(const char *buf, int sz)
	{
		DWORD snt = 0;
		iocp_overlapped *olp = new iocp_overlapped(buf, sz, _sock);
		if(WSASend(_sock, &(olp->_buf), 1, &snt, 0,&(olp->_overlapped), NULL) == SOCKET_ERROR)
		{
			int eno = WSAGetLastError();
			if(eno != WSA_IO_PENDING)
			{
				delete olp;
				return -1;
			}
		}

		return (int)snt;
	}

	int iocp_handler::async_recv(int sz)
	{
		DWORD rcv = 0;
		DWORD flag = 0;
		iocp_overlapped *olp = new iocp_overlapped(sz, _sock);
		if(WSARecv(_sock, &(olp->_buf), 1, &rcv, &flag, &(olp->_overlapped), NULL) == SOCKET_ERROR)
		{
			int eno = WSAGetLastError();
			if(eno != WSA_IO_PENDING)
			{
				delete olp;
				return -1;
			}
		}

		return (int)rcv;
	}
}

