#ifndef _LINUX_NETSVC_TYPE_H
#define _LINUX_NETSVC_TYPE_H
#include <string.h>
#include <arpa/inet.h>
namespace netsvc{
	/*udp dgram packet class*/
	class dpacket_t
	{
		friend class udp_receiver;

	public:
		dpacket_t(int bsz):_bsz(bsz),_dsz(0)
		{
			memset(&_addr, 0, sizeof(_addr));
			_buf = new char[bsz];
		}

		~dpacket_t()
		{
			delete []_buf;
			_buf = NULL;
		}

		/*set the data of the packet*/
		void set(const char *data, int sz)
		{
			int csz = sz>_bsz?_bsz:sz;
			memcpy(_buf, data, csz);
			_dsz = csz;
		}

		/*set the peer address relate with the packet*/
		inline void addr(const struct sockaddr *a)
		{
			memcpy(&_addr, a, sizeof(struct sockaddr));
		}

		/*return the peer address relate with the packet*/
		inline const struct sockaddr* addr()const
		{
			return &_addr;
		}

		/*return the host address ip relate with the packet*/
		inline const unsigned int ip()const
		{
			return ntohl(((struct sockaddr_in*)&_addr)->sin_addr.s_addr);
		}

		/*return the host address port relate with the packet*/
		inline const unsigned short port()const
		{
			return ntohs(((struct sockaddr_in*)&_addr)->sin_port);
		}

		/*get the write or read pointer for the buffer of packet object*/
		inline char *wptr()
		{
			return _buf;
		}

		inline const char *rptr()const 
		{
			return _buf;
		}

		/*get&set the buffer size or data size of the packet object*/
		inline const int bsz()const
		{
			return _bsz;
		}

		inline const int dsz()const
		{
			return _dsz;
		}

		inline void dsz(int sz)
		{
			_dsz =sz;
		}

	private:
		/*peer information relate with the packet*/
		//peer address
		struct sockaddr _addr;

		//data buffer
		char *_buf;
		//size of buffer
		int _bsz;
		//length of data in buffer
		int _dsz;
	};

	/*queue element for read&write queue*/
	class netsvc_qrdwr{
	public:
		netsvc_qrdwr():_valptr(0){}
		~netsvc_qrdwr(){}

		inline void setval(void *ptr)
		{
			_valptr = ptr;
		}

		inline void getval(void *&ptr)
		{
			ptr = _valptr;
		}

	private:
		//actual value the queue element hold
		void* _valptr;
	};
}
#endif

