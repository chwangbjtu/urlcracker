#include "en_interface.h"
#include <iostream>
#include "encrypt_crack.h"

encrypt_base* g_p_encrypt_crack = encrypt_crack::instance();

int ftsps::decrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len) 
{
	return g_p_encrypt_crack->decrypt(a_index, k_index, random, pkt, len);
}

int ftsps::encrypt(int a_index, int k_index, unsigned int random, unsigned char* pkt, int len) 
{
	return g_p_encrypt_crack->encrypt(a_index, k_index, random, pkt, len);
} 	

