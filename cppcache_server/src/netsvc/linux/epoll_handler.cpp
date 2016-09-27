#include "linux/epoll_handler.h"
namespace netsvc{
	epoll_handler::epoll_handler():_sock(-1),_ip(0),_port(0),_timer_tm((time_t)(-1)),_userarg(NULL)
	{
	}

	epoll_handler::~epoll_handler(void)
	{
		if(_sock != -1)
			close(_sock);
		_sock = -1;
	}

	int epoll_handler::handle_open(void *arg)
	{
		return -1;
	}

	int epoll_handler::handle_send()
	{
		return -1;
	}

	int epoll_handler::handle_recv()
	{
		return -1;
	}

	int epoll_handler::handle_error(int err)
	{
		return -1;
	}

	int epoll_handler::handle_close()
	{
		return -1;
	}

	int epoll_handler::handle_shutd()
	{
		return 0;
	}

	int epoll_handler::handle_timeout()
	{
		return 0;
	}

	int epoll_handler::handle_run(time_t tm)
	{
		return 0;
	}

	ssize_t epoll_handler::send(const void*buffer, size_t length, int flags)
	{
		return ::send(_sock, buffer, length, flags);
	}

	ssize_t epoll_handler::recv(char *buffer, int length, int flags)
	{
		return ::recv(_sock, buffer, length, flags);
	}
}

