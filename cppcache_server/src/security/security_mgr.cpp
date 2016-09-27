#include "security_mgr.h"
#include "en_interface.h"
#include "configure.h"
#include "stdlib.h"
#include "k_str.h"
#include <iostream>

#define PRIVATEKEY "etc/private.key"

security_mgr* security_mgr::_inst = NULL;
security_mgr::security_mgr()
{  
}

security_mgr::~security_mgr()
{  
    vector<security_util*>::iterator iter = _utils.begin();
    for (; iter != _utils.end(); ++iter) {
        if (*iter != NULL) {
            delete *iter;
            *iter = NULL;
        }
    }
    _utils.clear();
}

security_mgr* security_mgr::instance()
{
    if (_inst == NULL) {
        _inst = new security_mgr();
    }
    return _inst;
}

void security_mgr::del_instance()
{
    if (_inst != NULL) {
        delete _inst;
        _inst = NULL;
    }
}

int security_mgr::encrypt_rsa_base64(string& source, string& dest, unsigned int tid)
{
    return 0;
    int res = 0;
    string encrypted;
    security_util * util = get_security_util(tid);
    res = util->rsa_encrypt((char*)source.c_str(), source.length(), PRIVATEKEY, encrypted);
    if (res != 0) {
        cout << "加密出错" << endl;
        return -1;
    }
    
    char* base64_encode_output = NULL;
    util->base64_encode((unsigned char*)encrypted.c_str(), encrypted.length(), &base64_encode_output);
    string based(base64_encode_output);
    dest = based;
    if (base64_encode_output) {
        free(base64_encode_output);
        base64_encode_output = NULL;
    }
    return 0;
}

int security_mgr::decrypt_rsa_base64(string& source, string& dest, unsigned int tid)
{
    unsigned char* decode_str = NULL;
    size_t test;
    security_util * util = get_security_util(tid);
    util->base64_decode((char*)source.c_str(), &decode_str, &test);
    
    int res = util->rsa_decrypt((char*)decode_str, test, PRIVATEKEY, dest);
    if (decode_str) {
        free(decode_str);
        decode_str = NULL;
    }

    if (res != 0) {
        cout << "解密失败" << res << endl;
        return -1;
    }
    return 0;
}

int security_mgr::encrypt_xor(encrypt_t& info, unsigned int tid)
{
    if (info.encrypt_str.empty()) {
        return -1;
    }
    
    info.a_index = 1;
    info.k_index = rand() & 0x000F; 
    info.random = rand() & 0xFFFF;
    
    int res = ftsps::encrypt(info.a_index, info.k_index, info.random, (unsigned char*)info.encrypt_str.c_str(), info.encrypt_str.length());
    if (res == 0) {
        return -1;
    }
    
    security_util * util = get_security_util(tid);
    char* base64_encode_output = NULL;
    util->base64_encode((unsigned char*)info.encrypt_str.c_str(), info.encrypt_str.length(), &base64_encode_output);
    string based(base64_encode_output);
    if (base64_encode_output) {
        free(base64_encode_output);
        base64_encode_output = NULL;
    }
    
    //ftsps::decrypt(info.a_index, info.k_index, info.random, (unsigned char*)info.encrypt_str.c_str(), info.encrypt_str.length());
    
    info.encrypt_str.clear();
    info.encrypt_str = based;
    
    return 0;
}

int security_mgr::decrypt_xor(encrypt_t& info, unsigned int tid)
{
    ftsps::decrypt(info.a_index, info.k_index, info.random, (unsigned char*)info.encrypt_str.c_str(), info.encrypt_str.length());
    return 0;
}

string security_mgr::get_md5(string& source, unsigned int tid)
{
    return get_security_util(tid)->get_md5(source);
}

int security_mgr::base64_decode(char* b64_msg, unsigned char** buffer, size_t* length, unsigned int tid)
{
    security_util * util = get_security_util(tid);
    util->base64_decode(b64_msg, buffer, length);
    return 0;
}

security_util* security_mgr::get_security_util(unsigned int thread_id)
{
    if (_utils.empty() || (thread_id + 1) > _utils.size()) {
        return NULL;
    }
    return _utils[thread_id];
}

int security_mgr::start()
{
    // create multi security_util obj in case of openssl crash in multi-thread
    int thread_num = configure::instance()->get_service_worker_num();
    for (int i = 0; i < thread_num; ++i) {
        security_util* util = new security_util();
        if (util != NULL) {
            _utils.push_back(util);
        }
    }
    if (_utils.size() != thread_num) {
        return -1;
    }
    return 0;
}
