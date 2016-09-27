#ifndef _WIN_NETSVCRDWRQ_H
#define _WIN_NETSVCRDWRQ_H
#include "win/netsvc_type.h"
#include <Windows.h>

namespace netsvc{
	/*
	*	read write queue which is thread safe for only one reader & writer.
	*no lock used, it has high performance. it work best if make sure the 
	*reader is faster than the writer
	*
	*	!!notes!!:
	*	please adjust "queue size" for a good performance under different 
	*platform with different hardware, like: CPU.
	*/
	class netsvc_rdwrq
	{
	public:
		netsvc_rdwrq();
		netsvc_rdwrq(unsigned long qsz);
		~netsvc_rdwrq();

		/*
		*	initialize the queue with queue size @qsz
		*@param qsz: queue size
		*return:
		*	0--success, -1--failed
		*/
		int init(unsigned long qsz);

		/*
		*	read a value from queue in block mode until read success
		*@param ptr: in & out pointer to the read value
		*@param waittm: million seconds for read waiting
		*return:
		*	0--always success, -1--failed
		*/
		int read(void *&ptr, int waittm=-1);

		/*
		*	write a value to the queue in block mode until write success
		*@param ptr: pointer value to write
		*@param waittm: million seconds for write waiting
		*return:
		*	0--always success, -1--failed
		*/
		int write(void *ptr, int waittm=-1);

		/*
		*	read a value from queue in non-block mode
		*@param ptr: point to value if there is readable value in the queue
		*return:
		*	0--success, -1--no value has read, must wait
		*/
		int _read(void *&ptr);

		/*
		*	write a value into the queue in non-block mode
		*@param ptr: value to write
		*return:
		*	0--success, -1--no space can be used, must wait
		*/
		int _write(void *ptr);

	public:
		/*
		*	get the elements number in the queue
		*/
		unsigned int size()
		{
			volatile unsigned int num = _wpos-_rpos;
			return num;
		}

	private:
		/*
		*	expends a @val to power of 2. for example: 3->4, 7->8, 12->16, 21->32
		*/
		unsigned long roundup_power_of_two(unsigned long val);

	private:
		//queue size
		unsigned long _qsize;

		//queue array
		netsvc_qrdwr* _queue;

		//wait flag for read operation
		volatile long _rwflag;

		//wait flag for write operation
		volatile long _wwflag;

		//current read position of queue array
		volatile unsigned long _rpos;

		//next write position of queue array
		volatile unsigned long _wpos;

		//wait condition when read position catch the write position
		HANDLE _cond1;
		//wait condition when write position catch the read position
		HANDLE _cond2;
	};
}
#endif
