#include "client_req_struct.h"
#include "redis_mgr.h"
#include "tlogger.h"
#include "json_converter.h"
#include "fp_crack_v2_handler.h"
#include "security_mgr.h"
#include "md5.h"

fp_crack_v2_handler::fp_crack_v2_handler()
{
}

fp_crack_v2_handler::~fp_crack_v2_handler()
{
}

int fp_crack_v2_handler::process(const fs::http_request& hr,unsigned int ip,string& svid,string& parsestr,string& resp,unsigned int tid)
{
    int res = 0;
    req_struct_t treq;
    string info = hr._req._content;
    string decrpyted_str;
    string uid;
    string paramstr = hr._req._paramstr;
    res = get_uid(paramstr, uid);
    if (uid.empty()) {
        return -1;
    }
    
    res = security_mgr::instance()->decrypt_rsa_base64(info, decrpyted_str, tid);
    if (res != 0) {
        return -1;
    }
    
    KeyValue result;
    //cout << tid << decrpyted_str << endl;
    res = check_param(decrpyted_str, uid, result, tid);
    if (res != 0) {
        return -1;
    }
    
    treq._body = decrpyted_str;
    string vid = result["vid"];
    string site = result["site"];
    string url = result["url"];

    string data;
    //string skey = "crack:" + site + ":" + vid;
    string skey = "crack:" + site + ":" + vid + ":" + md5(url.substr(0, url.find("?")));
    if (skey.size() > 0)
    {
        svid = skey;
        redis_mgr::instance()->get_data(skey, data);
    }
    if (data.size() > 0 )
    {
        resp = data;
    }
    else
    {
        string task;
        build_task(result, task);
        redis_mgr::instance()->push_list_data(task);
        treq._hit = 0;
    }

    treq._vid = skey;
    treq._ip = ip;
    treq._type = 0;
    tlogger::instance()->log(treq);

	return 0;
}
