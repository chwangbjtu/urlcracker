#include "../security/include/security_mgr.h"
#include <iostream>
#include <unistd.h>
#include "json/json.h"
#include "curl/curl.h"
#include "stdlib.h"
#include "k_str.h"
#include <time.h>
#include <string.h>

#define PUBLIC "../../bin/etc/public.key"
#define PRIVATE "../../bin/etc/private.key"

using namespace std;

static size_t OnWriteData(void* buffer, size_t size, size_t nmemb, void* lpVoid)
{
    string* str = dynamic_cast<std::string*>((string*)lpVoid);
    if( NULL == str || NULL == buffer )
    {
        return -1;
    }

    char* pData = (char*)buffer;
    str->append(pData, size * nmemb);
    return nmemb;
}

int Post(const string& strUrl, const string& strPost, string& strResponse)
{
    CURLcode res;
    CURL* curl = curl_easy_init();
    if(NULL == curl)
    {
        return CURLE_FAILED_INIT;
    }

    curl_easy_setopt(curl, CURLOPT_URL, strUrl.c_str());
    curl_easy_setopt(curl, CURLOPT_POST, 1);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, strPost.c_str());
    curl_easy_setopt(curl, CURLOPT_READFUNCTION, NULL);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, OnWriteData);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&strResponse);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 3);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10);
    res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
    return res;
}

string encrypt_v2(string& source)
{
    string based;
    security_mgr::instance()->encrypt_rsa_base64(source, based);
    return based;
}

string encrypt_v3(string& source)
{
    return source;
}

string decrypt_v3(string ret_str)
{
    Json::Reader reader;
    Json::Value value;
    if (!reader.parse(ret_str, value) || value.type() != Json::objectValue ) {
        return "";
    }
    
    encrypt_t info;
    string encrypt_str = value["d"].asString();
    
    unsigned char* decode_str = NULL;
    size_t test;
    security_mgr::instance()->base64_decode((char*)encrypt_str.c_str(), &decode_str, &test);
    
    info.encrypt_str.resize(test);
    memcpy(&info.encrypt_str[0], decode_str, test);
    if (decode_str) {
        free(decode_str);
        decode_str = NULL;
    }
    info.a_index = atoi(value["a"].asString().c_str());
    info.k_index = atoi(value["b"].asString().c_str());
    info.random = (unsigned short)atoi(value["c"].asString().c_str());
    
    security_mgr::instance()->decrypt_xor(info);
    cout << info.encrypt_str << endl;
    return info.encrypt_str;
}

int main(int argc, char** argv)
{
    security_mgr::instance()->start();
    int oc;
    string vid;
    string site;
    string url;
    string os;
    string banben;
    string uid = "lalalala";
    
    while((oc = getopt(argc, argv, "v:s:o:u:b:")) != -1)
    {
        switch(oc) {
            case 'v':
                vid = optarg;
                break;
            case 's':
                site = optarg;
                break;
            case 'o':
                os = optarg;
                break;
            case 'u':
                url = optarg;
                break;
            case 'b':
                banben = optarg;
                break;
            default:
                break;
        }
    }
    
    Json::Value value;
    value["vid"] = vid;
    value["site"] = site;
    value["url"] = url;
    value["os"] = os;
    
    string beforo_md5 = vid + url + site + os + uid;
    string after_md5 = security_mgr::instance()->get_md5(beforo_md5);
    value["k"] = after_md5;
    
    Json::FastWriter writer;
    string json_msg = writer.write(value);
    string based = encrypt_v3(json_msg);
    
    time_t t;
    t = time(NULL);

    string s;
    s.resize(128, 0);
    sprintf(&s[0], "%ld", t);
    
    //string req_url = "http://suv.fun.tv/ck/" + banben + "?uid=" + uid + "&tm=" + s;
    string req_url = "http://192.168.16.159:8088/ck/" + banben + "?uid=" + uid + "&tm=" + s;
    //string req_url = "http://111.161.35.199:7410/ck/" + banben + "?uid=" + uid + "&tm=" + s;
    cout << req_url << endl;
    
    string ret_str;
    cout << based << endl;
    int ret = Post(req_url, based, ret_str);
    cout <<ret_str << endl;

    decrypt_v3(ret_str);
    return ret;
}
