#ifndef _WIN_IOCP_WORKER_H
#define _WIN_IOCP_WORKER_H
#include <map>
#include "win/netsvc_rdwrq.h"
#include "win/iocp_handler.h"
using namespace std;
namespace netsvc{
	class iocp_worker
	{
	public:
		iocp_worker(void);
		virtual ~iocp_worker(void);

		//stop iocp worker
		int start(int maxconns, int maxevents, int maxwaitm);

		//stop iocp worker
		int stop();

		//dispatch a iocp handler to this worker
		int dispatch(iocp_handler *hd);

		//concurrent connections in the worker
		unsigned int concurrency();

	private:
		//accept the new connection dispatched from accepter
		int accept();

		//remove a handler with socket @s from handle list
		int remove(SOCKET s);

		//run all handlers
		void run_handlers();

		//free all handlers
		void free_handlers();

		//get handler relate with socket
		iocp_handler *handler(SOCKET s);

		//reset the concurrency
		void reset_concurrency();

		//iocp worker thread
		static unsigned __stdcall work_thread(void *arg);

	private:
		//IOCP handler
		HANDLE _iocp;

		//pending handlers wait for add the iocp
		netsvc_rdwrq _pendq;

		//handler list in the iocp
		map<SOCKET, iocp_handler*> _handlers;

		//worker thread handler
		HANDLE _hdl;
		//worker thread id
		unsigned _thread_id;
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


