#include <time.h>
#include <errno.h>
#include "linux/netsvc_rdwrq.h"

namespace netsvc{
	netsvc_rdwrq::netsvc_rdwrq():_qsize(0),_queue(NULL),_rwflag(0),_wwflag(0),_rpos((unsigned long)-1),_wpos((unsigned long)-1)
	{

	}

	netsvc_rdwrq::netsvc_rdwrq(unsigned long qsz)
	{
		/*initial value of queue*/
		_qsize = roundup_power_of_two(qsz);

		/*allocate the queue buffer*/
		_queue = new netsvc_qrdwr[_qsize];

		/*initialize the read&write wait flag*/
		_rwflag = 1;
		_wwflag = 0;

		/*initialize the read&write position*/
		_rpos = 0;
		_wpos = 0;

		/*initialize the semaphore variable*/
		int err = sem_init(&_cond1, 0, 0);
		if(err != 0)
			cout<<"initial cycled read&write queue condition1 failed."<<endl;

		err = sem_init(&_cond2, 0, 0);
		if(err != 0)
			cout<<"initial cycled read&write queue condition2 failed."<<endl;
	}

	netsvc_rdwrq::~netsvc_rdwrq()
	{
		if(_queue != NULL)
			delete []_queue;
		_queue = 0;

		sem_destroy(&_cond1);
		sem_destroy(&_cond2);
	}

	int netsvc_rdwrq::init(unsigned long qsz)
	{
		/*initial value of queue*/
		_qsize = roundup_power_of_two(qsz);

		/*allocate the queue buffer*/
		_queue = new netsvc_qrdwr[_qsize];
		if(_queue == NULL)
			return -1;

		/*initialize the read&write wait flag*/
		_rwflag = 1;
		_wwflag = 0;

		/*initialize the read&write position*/
		_rpos = 0;
		_wpos = 0;

		/*initialize the semaphore variable*/
		int err = sem_init(&_cond1, 0, 0);
		if(err != 0)
			cout<<"initial cycled read&write queue condition1 failed."<<endl;

		err = sem_init(&_cond2, 0, 0);
		if(err != 0)
			cout<<"initial cycled read&write queue condition2 failed."<<endl;

		return 0;
	}

	int netsvc_rdwrq::read(void *&ptr, int waittm/*=-1*/)
	{
		int wtm = 10;
		if(!(waittm<0))
			wtm = waittm;
		
		int err = _read(ptr);
		while(err != 0)
		{
			_rwflag = 1;
			if(_wwflag == 1)
			{
				_wwflag = 0;
				sem_post(&_cond2);
			}

			struct timespec tw;
			get_waittm(&tw, wtm);
			int res = sem_timedwait(&_cond1, &tw);
			if(res==-1 && !(waittm<0) && errno==ETIMEDOUT)
			{
				err = _read(ptr);
				break;
			}
		
			err = _read(ptr);
		}

		if(_wwflag == 1)
		{
			_wwflag = 0;
			sem_post(&_cond2);
		}

		if(err != 0)
			return -1;

		return 0;
	}

	int netsvc_rdwrq::write(void *ptr, int waittm/*=-1*/)
	{
		int wtm = 10;
		if(!(waittm<0))
			wtm = waittm;

		int err = _write(ptr);
		while(err != 0)
		{
			_wwflag = 1;
			if(_rwflag == 1)
			{
				_rwflag = 0;
				sem_post(&_cond1);
			}

			struct timespec tw;
			get_waittm(&tw, wtm);
			int res=sem_timedwait(&_cond2, &tw);
			if(res==-1 && !(waittm<0) && errno == ETIMEDOUT)
			{
				err = _write(ptr);
				break;
			}

			err = _write(ptr);
		}

		if(_rwflag == 1)
		{
			_rwflag = 0;
			sem_post(&_cond1);
		}

		if(err != 0)
			return -1;

		return 0;
	}

	int netsvc_rdwrq::_read(void *&ptr)
	{
		unsigned long fillsz = _wpos-_rpos;

		if(fillsz != 0)
		{
			unsigned long rpos = _rpos & (_qsize-1);
			_queue[rpos].getval(ptr);
			_rpos++;
		}
		else
			return -1;

		return 0;
	}

	int netsvc_rdwrq::_write(void *ptr)
	{
		unsigned long leftsz = _qsize-_wpos+_rpos;

		if(leftsz != 0)
		{
			unsigned long wpos = _wpos & (_qsize-1);
			_queue[wpos].setval(ptr);
			_wpos++;
		}
		else
			return -1;

		return 0;
	}

	int netsvc_rdwrq::get_waittm(struct timespec *tw, int elapse)
	{
		clock_gettime(CLOCK_REALTIME, tw);
		tw->tv_sec += (time_t)(elapse/1000);	
		tw->tv_nsec += ((long)(elapse%1000))*1000*1000;
		if(tw->tv_nsec >= 1000*1000*1000)
		{
			tw->tv_sec += 1;
			tw->tv_nsec -= 1000*1000*1000;
		}

		return 0;
	}

	unsigned long netsvc_rdwrq::roundup_power_of_two(unsigned long val)
	{
		/*val is the power of 2*/
		if((val & (val-1)) == 0)
			return val;

		/*expand val to power of 2*/
		unsigned long maxulong = (unsigned long)((unsigned long)~0);
		unsigned long andv = ~(maxulong&(maxulong>>1));
		while((andv & val) == 0)
			andv = andv>>1;

		return andv<<1;
	}
}

