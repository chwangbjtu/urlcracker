#ifndef _LINUX_EPOLL_HANDLER_H
#define _LINUX_EPOLL_HANDLER_H
#include <time.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
namespace netsvc{
	/*abstract handler for epoll accepter & connector*/
	class epoll_handler
	{
	public:
		epoll_handler();
		virtual ~epoll_handler(void);

		/*
		*	recall method after the connection has build, the @arg is
		*passed to the accepter when start the service.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_open(void *arg);

		/*
		*	recall method when the epoll write edge triggered, send data
		*until can not send.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_send();

		/*
		*	recall method when the epoll read edge triggered, receive data
		*until no data could be received.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_recv();

		/*
		*	recall method when error happened on the socket
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_error(int err);

		/*
		*	recall method before socket closed, always invoked before the
		*handler destroyed.
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_close();

		/*
		*	recall method when peer shutdown the send channel. which means
		*fin packet received
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_shutd();

		/*
		*	recall method when timer triggered. timer event is set
		*by calling the @set_timeout method
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_timeout();

		/*
		*	recall method every tiny period
		*return:
		*	0--success, other--failed, handler will be destroyed
		*/
		virtual int handle_run(time_t tm);

	public:
		inline void sock(int sk)
		{
			_sock = sk;
		}

		inline int sock() const
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

        inline void thread_index(int thread_index)
        {
            _thread_index = thread_index;
        }

        inline int thread_index()
        {
            return _thread_index;
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

			return true;
		}

	protected:
		/*send data to peer*/
		ssize_t send(const void*buffer, size_t length, int flags);
		/*received data from peer*/
		ssize_t recv(char *buffer, int length, int flags);
        //
        int _thread_index;

	private:
		//socket of the relate handler
		int _sock;
		//remote peer ip
		unsigned int _ip;
		//remote peer port
		unsigned short _port;

		//timer trigger timestamp
		time_t _timer_tm;


		//user argument, only used in accepter
		void *_userarg;
	};
}
#endif

