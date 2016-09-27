#ifndef __ENCRYPT_CRACK_H__
#define __ENCRYPT_CRACK_H__

#include "encrypt_base.h"
namespace ftsps {

//class encryption;
class encrypt_crack : public encrypt_base{
public:
	virtual ~encrypt_crack(){}
	static encrypt_crack* instance(void);
private:	
	encrypt_crack();
	static encrypt_crack* _instance;
};

//class arithmetic;
class arithmetic_crack1 : public arithmetic_base{
public:
	friend class encrypt_crack;
	arithmetic_crack1();
	virtual ~arithmetic_crack1();
    
protected:
	virtual int decrypt(int k_index, unsigned int random, unsigned char* pkt, int len);
	virtual int encrypt(int k_index, unsigned int random, unsigned char* pkt, int len);
private:
	inline int xxcrypt(int k_index, unsigned int random, unsigned char* pkt, int len);
};

//class register;
class register_encrypt_crack {
public:
	register_encrypt_crack(){encrypt_crack::instance();}
};

};
using namespace ftsps;
#endif//__ENCRYPT_CRACK_H__:~~

