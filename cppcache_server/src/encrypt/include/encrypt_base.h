#ifndef __ENCRYPT_BASE_H__
#define __ENCRYPT_BASE_H__

#include <stdio.h>

namespace ftsps {

class arithmetic_base {
	friend class encrypt_base;
protected:
	unsigned char* _secret_key;	
	virtual int decrypt(int k_index, unsigned int random, unsigned char* pkt, int len) = 0;
	virtual int encrypt(int k_index, unsigned int random, unsigned char* pkt, int len) = 0; 
public:
	arithmetic_base(){}
	virtual ~arithmetic_base(){}
};

class encrypt_base  {
protected:
	arithmetic_base*	_arithmetic[16];	

public:
	encrypt_base(){for (int i = 0; i < 16; ++i) _arithmetic[i] = NULL;}
	virtual ~encrypt_base(){}

	int register_arithmetic(int index, arithmetic_base* arith);	
	virtual int decrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len); 
	virtual int encrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len); 	
};

};
using namespace ftsps;
#endif//__ENCRYPT_BASE_H__:~~


