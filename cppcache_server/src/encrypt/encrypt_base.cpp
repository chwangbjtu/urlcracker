#ifdef _WIN32
#include <winsock2.h>
#else// _WIN32
#include <arpa/inet.h>
#endif// _WIN32:~~
#include <string.h>
#include <stdlib.h>
#include "encrypt_base.h"

int 
encrypt_base::register_arithmetic(int index, arithmetic_base* arith) 
{
	if (index & 0xFFFFFFF0) {
		return -1;
	}
	if (!_arithmetic[index] && arith ) {
		_arithmetic[index] = arith;
		return 0;	
	} 
	return -2;
}

int 
encrypt_base::decrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len) 
{
	/*check*/
	if ( !_arithmetic[a_index] ) { 
		return 0; 
	} 
	
	/*decryption*/
	return _arithmetic[a_index]->decrypt(k_index, random, pkt, len);
}

int 
encrypt_base::encrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len) 
{	
	/*check input*/
	if ( !_arithmetic[a_index] ) { 
		return 0; 
	} 

	/*encryption*/
	return _arithmetic[a_index]->encrypt(k_index, random, pkt, len);
} 
