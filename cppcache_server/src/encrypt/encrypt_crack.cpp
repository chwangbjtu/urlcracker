#include "encrypt_crack.h"
#include "encrypt_base.h"
#include <malloc.h>
#include <stdio.h>

#define KEY_LEN1 128
arithmetic_crack1::arithmetic_crack1(){
	_secret_key = (unsigned char*)malloc(KEY_LEN1);
	_secret_key[0] = 0xDC;_secret_key[1] = 0x47;_secret_key[2] = 0xE2;_secret_key[3] = 0xA6;
	_secret_key[4] = 0x0D;_secret_key[5] = 0x70;_secret_key[6] = 0x71;_secret_key[7] = 0x21;
	_secret_key[8] = 0x6D;_secret_key[9] = 0x21;_secret_key[10] = 0x28;_secret_key[11] = 0xDD;
	_secret_key[12] = 0xD1;_secret_key[13] = 0x6D;_secret_key[14] = 0x20;_secret_key[15] = 0xA4;
	_secret_key[16] = 0xAC;_secret_key[17] = 0x88;_secret_key[18] = 0x0A;_secret_key[19] = 0x75;
	_secret_key[20] = 0xD5;_secret_key[21] = 0x7F;_secret_key[22] = 0x12;_secret_key[23] = 0xD4;
	_secret_key[24] = 0x8A;_secret_key[25] = 0x26;_secret_key[26] = 0x0A;_secret_key[27] = 0x65;
	_secret_key[28] = 0xB4;_secret_key[29] = 0x52;_secret_key[30] = 0xC4;_secret_key[31] = 0xB9;
	_secret_key[32] = 0x6C;_secret_key[33] = 0x49;_secret_key[34] = 0xBF;_secret_key[35] = 0x68;
	_secret_key[36] = 0xBF;_secret_key[37] = 0x77;_secret_key[38] = 0x06;_secret_key[39] = 0x60;
	_secret_key[40] = 0xAE;_secret_key[41] = 0x63;_secret_key[42] = 0x56;_secret_key[43] = 0x7C;
	_secret_key[44] = 0x79;_secret_key[45] = 0xE1;_secret_key[46] = 0x7F;_secret_key[47] = 0x59;
	_secret_key[48] = 0x1E;_secret_key[49] = 0x88;_secret_key[50] = 0x0C;_secret_key[51] = 0x65;
	_secret_key[52] = 0x1C;_secret_key[53] = 0x66;_secret_key[54] = 0x26;_secret_key[55] = 0x38;
	_secret_key[56] = 0x7C;_secret_key[57] = 0xF3;_secret_key[58] = 0xB6;_secret_key[59] = 0x28;
	_secret_key[60] = 0x12;_secret_key[61] = 0x44;_secret_key[62] = 0xCA;_secret_key[63] = 0x17;
	_secret_key[64] = 0x01;_secret_key[65] = 0x81;_secret_key[66] = 0x3A;_secret_key[67] = 0x90;
	_secret_key[68] = 0x7D;_secret_key[69] = 0x99;_secret_key[70] = 0x8B;_secret_key[71] = 0x13;
	_secret_key[72] = 0xD5;_secret_key[73] = 0x34;_secret_key[74] = 0x13;_secret_key[75] = 0xAC;
	_secret_key[76] = 0xB0;_secret_key[77] = 0xEA;_secret_key[78] = 0x5E;_secret_key[79] = 0xCA;
	_secret_key[80] = 0x96;_secret_key[81] = 0xB2;_secret_key[82] = 0xD1;_secret_key[83] = 0x4F;
	_secret_key[84] = 0xB3;_secret_key[85] = 0x9D;_secret_key[86] = 0x8D;_secret_key[87] = 0xE4;
	_secret_key[88] = 0xD8;_secret_key[89] = 0xC4;_secret_key[90] = 0x97;_secret_key[91] = 0x8F;
	_secret_key[92] = 0xC3;_secret_key[93] = 0x7E;_secret_key[94] = 0x35;_secret_key[95] = 0x87;
	_secret_key[96] = 0xA0;_secret_key[97] = 0xD7;_secret_key[98] = 0x9B;_secret_key[99] = 0x47;
	_secret_key[100] = 0xD0;_secret_key[101] = 0x3E;_secret_key[102] = 0xC6;_secret_key[103] = 0xE1;
	_secret_key[104] = 0xE8;_secret_key[105] = 0x7E;_secret_key[106] = 0xA9;_secret_key[107] = 0x95;
	_secret_key[108] = 0xFD;_secret_key[109] = 0xF0;_secret_key[110] = 0x87;_secret_key[111] = 0xA2;
	_secret_key[112] = 0x1F;_secret_key[113] = 0xEE;_secret_key[114] = 0xA0;_secret_key[115] = 0x5C;
	_secret_key[116] = 0x23;_secret_key[117] = 0x8A;_secret_key[118] = 0x0F;_secret_key[119] = 0x7F;
	_secret_key[120] = 0xA6;_secret_key[121] = 0x80;_secret_key[122] = 0xF3;_secret_key[123] = 0xC3;
	_secret_key[124] = 0x4E;_secret_key[125] = 0x6A;_secret_key[126] = 0xCD;_secret_key[127] = 0xB0;
}

arithmetic_crack1::~arithmetic_crack1() {
	free(_secret_key);
}

inline int 
arithmetic_crack1::xxcrypt(int k_index, unsigned int random, unsigned char* pkt, int len)
{
	int key = k_index << 3; 
	unsigned int rand_key = (random << 16) | random;

	int i = key, j = 0, slen = len & 0xFFFFFFFC;

	for (; j < slen; i = 0) {
		for (; i < KEY_LEN1 - 4 && j < slen; i = i + 4, j = j + 4) {
			(*(int*)(&pkt[j])) ^= (*(int*)(&_secret_key[i])) ^ rand_key;
		}
	}

	if (slen < len) {
		for (i = key + slen; j < len; i = 0) {
			for (; i< KEY_LEN1 && j < len; i++, j++) {
				pkt[j] ^= _secret_key[i];
			}
		}	
	}

	return len;	
}

int 
arithmetic_crack1::encrypt(int k_index, unsigned int random, unsigned char* pkt, int len) 
{
	return xxcrypt(k_index, random, pkt, len);
}

int 
arithmetic_crack1::decrypt(int k_index, unsigned int random, unsigned char* pkt, int len) 
{
	return xxcrypt(k_index, random, pkt, len);
}

encrypt_crack* encrypt_crack::_instance = new encrypt_crack();
register_encrypt_crack g_register_encrypt_crack;

encrypt_crack*
encrypt_crack::instance(void)
{
	if (_instance == NULL) {
		_instance = new encrypt_crack();
	}
	return _instance;
}

encrypt_crack::encrypt_crack() 
{
	this->register_arithmetic(1, new arithmetic_crack1());
}

