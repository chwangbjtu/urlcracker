#include "win/netsvc_rdwrq.h"

namespace netsvc
{
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

		/*initialize the condition variable*/
		_cond1 = CreateEvent(NULL, FALSE, FALSE, NULL);
		_cond2 = CreateEvent(NULL, FALSE, FALSE, NULL);
	}

	netsvc_rdwrq::~netsvc_rdwrq()
	{
		if(_queue != NULL)
			delete []_queue;
		_queue = 0;

		CloseHandle(_cond1);
		CloseHandle(_cond2);
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

		/*initialize the condition variable*/
		_cond1 = CreateEvent(NULL, FALSE, FALSE, NULL);
		_cond2 = CreateEvent(NULL, FALSE, FALSE, NULL);

		return 0;
	}

	int netsvc_rdwrq::read(void *&ptr, int waittm/* =-1 */)
	{
		DWORD wtm = INFINITE;
		if(!(waittm < 0))
			wtm = waittm;

		int err = _read(ptr);
		while(err != 0)
		{
			_rwflag = 1;
			if(_wwflag == 1)
			{
				_wwflag = 0;
				SetEvent(_cond2);
			}

			DWORD res = WaitForSingleObject(_cond1, wtm);
			if(!(waittm<0) && res == WAIT_TIMEOUT)
			{
				err = _read(ptr);
				break;
			}
			
			err = _read(ptr);
		}

		if(_wwflag == 1)
		{
			_wwflag = 0;
			SetEvent(_cond2);
		}

		if(err != 0)
			return -1;

		return 0;
	}

	int netsvc_rdwrq::write(void *ptr, int waittm/* =-1 */)
	{
		DWORD wtm = INFINITE;
		if(!(waittm < 0))
			wtm = waittm;

		int err = _write(ptr);
		while(err != 0)
		{
			_wwflag = 1;
			if(_rwflag == 1)
			{
				_rwflag = 0;
				SetEvent(_cond1);
			}

			DWORD res = WaitForSingleObject(_cond2, wtm);
			if(!(waittm<0) && res==WAIT_TIMEOUT)
			{
				err = _write(ptr);
				break;
			}
			
			err = _write(ptr);
		}

		if(_rwflag == 1)
		{
			_rwflag = 0;
			SetEvent(_cond1);
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
