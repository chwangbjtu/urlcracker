#ifndef _WIN_IOCP_HANDLER_H
#define _WIN_IOCP_HANDLER_H
#include <time.h>
#include <WinSock2.h>
#include <Windows.h>

namespace netsvc{
	/*abstract iocp handler class for iocp accepter & connector*/
	class iocp_handler
	{
	public:
		iocp_handler();
		virtual ~iocp_handler(void);

		/*
		*	recalled when the connection has build, the @arg is the
		*parameter passed when the accepter started or specified by the
		*connector's connect method.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int on_open(void *arg);

		/*
		*	recalled when the the data has send out, with send size @sz_send.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int on_send(int sz_send);

		/*
		*	recalled when the the @data with size @sz_recv has received.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int on_recv(const char *data, int sz_recv);
		
		/*
		*	recalled when there is error happened on the connection, @err
		*is the errno return by the system.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int on_error(int err);
		
		/*
		*	recalled when the handler will be destroyed.
		*return:
		*	0--success, other--failed
		*/
		virtual int on_close();
		
		/*
		*	recalled when the timer has triggered.
		*return:
		*	0--success, other--failed
		*/
		virtual int on_timeout();

		/*
		*	recalled every tiny interval, make the instance to process
		*something.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int on_running(time_t tm);

	public:
		inline void sock(SOCKET sk)
		{
			_sock = sk;
		}

		inline SOCKET sock() const
		{
			return _sock;
		}

		inline void peer_ip(unsigned int ip)
		{
			_ip = ip;
		}

		inline unsigned int peer_ip()
		{
			return _ip;
		}

		inline void peer_port(unsigned short port)
		{
			_port = port;
		}

		inline unsigned short peer_port()
		{
			return _port;
		}

		inline void userarg(void *arg)
		{
			_userarg = arg;
		}

		inline void* userarg()
		{
			return _userarg;
		}

		/*set the timer delay time in seconds*/
		inline void set_timeout(int delay_secs)
		{
			_timer_tm = time(NULL)+delay_secs;
		}

		/*check is the timer should be triggered*/
		inline bool is_timeout(time_t now)
		{
			/*check the timer*/
			if(_timer_tm == ((time_t)-1))
				return false;
			
			if(_timer_tm > now)
				return false;

			/*set the timer invalid when triggered once*/
			_timer_tm = (time_t)(-1);

			return true;
		}

	protected:
		/*make an asynchronize iocp send operation with data @buf which size is @sz*/
		int async_send(const char *buf, int sz);
		/*make an asynchronize iocp receive operation with size @sz*/
		int async_recv(int sz);

	private:
		//socket of the relate handler
		SOCKET _sock;
		//remote peer ip
		unsigned int _ip;
		//remote peer port
		unsigned short _port;
		
		//timer trigger timestamp
		time_t _timer_tm;

		//user argument, only used in accepter
		void *_userarg;
	};

	/*iocp operation*/
	typedef enum{IOCP_SEND, IOCP_RECV, IOCP_INVALID} iocp_opt;

	/*self defined overlapped structure for iocp*/
	struct iocp_overlapped 
	{
		OVERLAPPED _overlapped;
		WSABUF _buf;
		iocp_opt _opt;
		SOCKET _sock;

		iocp_overlapped(const char *data, int send_sz, SOCKET sock):_opt(IOCP_SEND), _sock(sock)
		{
			_buf.len = send_sz;
			_buf.buf = new char[send_sz];
			memcpy(_buf.buf, data, send_sz);
			memset(&_overlapped, 0, sizeof(_overlapped));
		}

		iocp_overlapped(int recv_sz, SOCKET sock):_opt(IOCP_RECV), _sock(sock)
		{
			_buf.len = recv_sz;
			_buf.buf = new char[recv_sz];
			memset(&_overlapped, 0, sizeof(_overlapped));
		}

		~iocp_overlapped()
		{
			delete [](_buf.buf);
			_buf.len = 0;
			_opt = IOCP_INVALID;
		}
	};
}
#endif

