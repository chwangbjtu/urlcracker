#include "security.h"
#include <openssl/bio.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/md5.h>
#include <openssl/err.h>
#include <openssl/buffer.h>
#include <string.h>
#include <iostream>

#define MUTEX_TYPE pthread_mutex_t
#define MUTEX_SETUP(x) pthread_mutex_init(&(x), NULL)
#define MUTEX_CLEANUP(x) pthread_mutex_destroy(&(x))
#define MUTEX_LOCK(x) pthread_mutex_lock(&(x))
#define MUTEX_UNLOCK(x) pthread_mutex_unlock(&(x))
#define THREAD_ID pthread_self()

pthread_mutex_t security_util::_inst_mutex = PTHREAD_MUTEX_INITIALIZER;
security_util* security_util::_inst = NULL;
pthread_mutex_t* security_util::_mutex_buf = NULL;

security_util* security_util::instance()
{
    if (_inst == NULL) {
        pthread_mutex_lock(&_inst_mutex);
        if (_inst == NULL) {
            _inst = new security_util();
            if (_inst->thread_setup() != 0) {
                cout << "openssl 多线程初始化错误";
                //todo
            }
        }
        pthread_mutex_unlock(&_inst_mutex);
    }
    return _inst;
}

void security_util::del_instance()
{
    if (_inst != NULL) {
        pthread_mutex_lock(&_inst_mutex);
        if (_inst != NULL) {
            delete _inst;
            _inst = NULL;
        }
        pthread_mutex_unlock(&_inst_mutex);
    }
}

security_util::security_util()
{
}

security_util::~security_util()
{
    thread_cleanup();
}

int security_util::rsa_encrypt(char* str, int length, const char* path_key, string& encrypted)
{
    RSA* p_rsa;
    FILE* file;
    int rsa_len = 0;

    if ((file = fopen(path_key,"r")) == NULL) {
        return -1;
    }   
    if ((p_rsa = PEM_read_RSA_PUBKEY(file, NULL, NULL, NULL)) == NULL) {
        return -1;
    }
    
    rsa_len = RSA_size(p_rsa);
    int block_num = rsa_len - 11;
    while (length > 0) {
        size_t size = length >= block_num ? block_num : length;
        string tmp_encrypted;
        tmp_encrypted.resize(rsa_len, 0);
        int num = RSA_public_encrypt(size, (unsigned char*)str, (unsigned char*)&tmp_encrypted[0], p_rsa, RSA_PKCS1_PADDING);
        if (num != rsa_len){
            return -1;
        }
        encrypted += tmp_encrypted;
        str += size;
        length -= size;
    }

    RSA_free(p_rsa);
    fclose(file);

    return 0;
}

int security_util::rsa_decrypt(char* str, int length, const char* path_key, string& decrpyted)
{
    RSA* p_rsa;
    FILE* file;
    int rsa_len;
    if ((file = fopen(path_key,"r")) == NULL) {
        return -1;
    }
    if ((p_rsa = PEM_read_RSAPrivateKey(file, NULL, NULL, NULL)) == NULL) {
        return -1;
    }
    
    rsa_len = RSA_size(p_rsa);
    int block_num = rsa_len;
    while (length > 0) {
        size_t size = length >= block_num ? block_num : length;
        string tmp_decrpyted;
        tmp_decrpyted.resize(block_num - 11, 0);
        if (RSA_private_decrypt(rsa_len, (unsigned char*)str, (unsigned char*)&tmp_decrpyted[0], p_rsa, RSA_PKCS1_PADDING) < 0) {
            return -1;
        }
        
        decrpyted += tmp_decrpyted;
        str += size;
        length -= size;
    }
    
    RSA_free(p_rsa);
    fclose(file);
    return 0;
}

int security_util::base64_encode(const unsigned char* buffer, size_t length, char** b64_text)
{ 
    //Encodes a binary safe base 64 string
    BIO* bio = NULL;
    BIO* b64 = NULL;
    BUF_MEM* buffer_ptr = NULL;

    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new(BIO_s_mem());
    bio = BIO_push(b64, bio);

    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Ignore newlines - write everything in one line
    BIO_write(bio, buffer, length);
    BIO_flush(bio);
    BIO_get_mem_ptr(bio, &buffer_ptr);
    //BIO_set_close(bio, BIO_NOCLOSE);
    //*b64_text = (*buffer_ptr).data;
    
    int buffer_len = buffer_ptr->length;
    *b64_text = (char*)malloc(buffer_len + 1);
    (*b64_text)[buffer_len] = '\0';
    memcpy(*b64_text, buffer_ptr->data, buffer_len);
    
    BIO_set_close(bio, BIO_CLOSE);
    BIO_free_all(bio);
    return 0; //success
}

size_t security_util::calc_decode_length(const char* b64_input)
{ 
    //Calculates the length of a decoded string
    size_t len = strlen(b64_input);
    size_t padding = 0;

    if (b64_input[len - 1] == '=' && b64_input[len - 2] == '=') //last two chars are =
        padding = 2;
    else if (b64_input[len - 1] == '=') //last char is =
        padding = 1;

    return (len * 3) / 4 - padding;
}

int security_util::base64_decode(char* b64_msg, unsigned char** buffer, size_t* length)
{ 
    //Decodes a base64 encoded string
    BIO* bio = NULL;
    BIO* b64 = NULL;

    int decode_len = calc_decode_length(b64_msg);
    *buffer = (unsigned char*)malloc(decode_len + 1);
    (*buffer)[decode_len] = '\0';

    bio = BIO_new_mem_buf(b64_msg, -1);
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_push(b64, bio);

    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Do not use newlines to flush buffer
    *length = BIO_read(bio, *buffer, strlen(b64_msg));
    if (*length != decode_len) {
        return -1;
    }
    BIO_free_all(bio);

    return 0; //success
}

string security_util::get_md5(string& str)
{
    string result;
    result.resize(16, 0);
    
    MD5_CTX ctx;
    MD5_Init(&ctx);
    MD5_Update(&ctx, (char*)str.c_str(), str.length());
    MD5_Final((unsigned char*)&result[0], &ctx);
    
    return bin_2_hex(result);
}

string security_util::bin_2_hex(const string &str_bin, bool is_upper)
{
    string str_hex;
    str_hex.resize(str_bin.size() * 2);
    for (size_t i = 0; i < str_bin.size(); i++) {
        uint8_t temp = str_bin[i];
        for (size_t j = 0; j < 2; j++) {
            uint8_t cur = (temp & 0x0f);
            if (cur < 10) {
                cur += '0';
            }
            else {
                cur += ((is_upper ? 'A' : 'a') - 10);
            }
            str_hex[2 * i + 1 - j] = cur;
            temp >>= 4;
        }
    }

    return str_hex;
}

void security_util::locking_function(int mode, int n, const char* file, int line)
{
    if (mode & CRYPTO_LOCK)
        MUTEX_LOCK(_mutex_buf[n]);
    else
        MUTEX_UNLOCK(_mutex_buf[n]);
}

unsigned long security_util::id_function(void)
{
    return ((unsigned long)THREAD_ID);
}

int security_util::thread_setup(void)
{
    int i;
    _mutex_buf = (MUTEX_TYPE *) malloc(CRYPTO_num_locks() * sizeof(MUTEX_TYPE));
    if(!_mutex_buf)
        return -1;
    
    for (i = 0; i < CRYPTO_num_locks(); i++)
        MUTEX_SETUP(_mutex_buf[i]);
    
    CRYPTO_set_id_callback(id_function);
    CRYPTO_set_locking_callback(locking_function);
    return 0;
}

int security_util::thread_cleanup(void)
{
    int i;
    if (!_mutex_buf)
        return -1;
    
    CRYPTO_set_id_callback(NULL);
    CRYPTO_set_locking_callback(NULL);
    for (i = 0; i < CRYPTO_num_locks( ); i++)
        MUTEX_CLEANUP(_mutex_buf[i]);
    
    free(_mutex_buf);
    _mutex_buf = NULL;
    return 0;
}
