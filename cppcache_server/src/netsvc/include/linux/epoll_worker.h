#ifndef _LINUX_EPOLL_WORKER_H
#define _LINUX_EPOLL_WORKER_H
#include <map>
#include <pthread.h>
#include <sys/epoll.h>
#include "linux/netsvc_rdwrq.h"
#include "linux/epoll_handler.h"

//for checking the peer shutdown or close events, support from linux kernel 2.6.x
#ifndef EPOLLRDHUP
#define EPOLLRDHUP 0x2000
#endif


namespace netsvc{
	using namespace std;
	class epoll_worker
	{
	public:
		epoll_worker();
		virtual ~epoll_worker(void);

		//stop epoll worker
		int start(int maxconns, int maxevents, int maxwaitm,int threadindex);

		//stop epoll worker
		int stop();

		//dispatch a epoll handler to this worker
		int dispatch(epoll_handler *hd);

		//concurrent connections in the worker
		unsigned int concurrency();

	private:
		//accept the new connection dispatched from accepter
		int accept(int thread_index);

		//remove a handler with socket @s from handle list
		int remove(int sock);

		//run all handlers
		void run_handlers();

		//free all handlers
		void free_handlers();

		//reset the concurrency
		void reset_concurrency();

        //
        int thread_index();

		//iocp worker thread
		static void* work_thread(void *arg);

	private:
        //thread index
        int _thread_index;

		//epoll handler
		int _epoll_fd;

		//pending handlers wait for add the epoll
		netsvc_rdwrq _pendq;

		//handler list in the epoll
		map<int, epoll_handler*> _handlers;

		//worker thread handler
		pthread_t _thread_worker;
		//stop flag for worker thread
		bool _worker_stop;

		//max concurrence connections for the worker
		int _max_conns;
		//max events processed per time for worker
		int _max_events;
		//max wait time for the get iocp status
		int _max_waittm;

		//concurrent connections
		volatile unsigned int _concurrency;
	};

	typedef enum{round, least}dispatch_t;
}
#endif

