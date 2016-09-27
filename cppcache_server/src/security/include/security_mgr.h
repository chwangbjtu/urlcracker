#ifndef __SECURITY_MGR_H
#define __SECURITY_MGR_H

#include "security.h"
#include <vector>
using namespace std;

typedef struct encrypt {
    int a_index;
    int k_index;
    unsigned int random;
    string encrypt_str;
    
} encrypt_t;

class security_mgr
{
public:
    static security_mgr* instance();
    static void del_instance();
    
    int start();
    int encrypt_rsa_base64(string& source, string& dest, unsigned int tid = 0);
    int decrypt_rsa_base64(string& source, string& dest, unsigned int tid = 0);
    int encrypt_xor(encrypt_t& info, unsigned int tid = 0);
    int decrypt_xor(encrypt_t& info, unsigned int tid = 0);
    string get_md5(string& source, unsigned int tid = 0);
    int base64_decode(char* b64_msg, unsigned char** buffer, size_t* length, unsigned int tid = 0);

private:
    security_mgr();
    ~security_mgr();
    security_util* get_security_util(unsigned int thread_id = 0);
    
    vector<security_util*> _utils;
    static security_mgr* _inst;
};

#endif
