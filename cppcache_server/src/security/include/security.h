#ifndef __SECURITY_UTIL_H
#define __SECURITY_UTIL_H

#include <string>
#include <pthread.h>
using namespace std;
typedef unsigned char uint8_t;

class security_util
{
public:
    security_util();
    ~security_util();
    // do not use this!!!!!
    static security_util* instance();
    static void del_instance();
    
    int rsa_encrypt(char* str, int length, const char* path_key, string& encrypted);
    int rsa_decrypt(char* str, int length, const char* path_key, string& decrpyted);
    int base64_encode(const unsigned char* buffer, size_t length, char** b64_text);
    int base64_decode(char* b64_msg, unsigned char** buffer, size_t* length);
    string get_md5(string& str);
    string bin_2_hex(const string& str_bin, bool is_upper = false);
    
private:
    //security_util();
    //~security_util();
    security_util(const security_util&);
    security_util& operator=(const security_util&);
    size_t calc_decode_length(const char* b64_input);
    
    // functions for thread safe
    int thread_setup(void);
    int thread_cleanup(void);
    static void locking_function(int mode, int n, const char* file, int line);
    static unsigned long id_function(void);
    
    static security_util* _inst;
    static pthread_mutex_t _inst_mutex;
    static pthread_mutex_t* _mutex_buf;
};

#endif
