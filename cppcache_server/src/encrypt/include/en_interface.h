#ifndef __I_ENCRYPTION_H__
#define __I_ENCRYPTION_H__

#include "stdio.h"
namespace ftsps {
	int decrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len);
	int encrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len);
};

using namespace ftsps;
#endif//__I_ENCRYPTION_H__:~~

