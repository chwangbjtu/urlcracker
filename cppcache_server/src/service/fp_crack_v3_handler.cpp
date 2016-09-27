#include "client_req_struct.h"
#include "redis_mgr.h"
#include "slave_mgr.h"
#include "tlogger.h"
#include "json_converter.h"
#include "fp_crack_v3_handler.h"
#include "security_mgr.h"
#include "util.h"
#include "md5.h"

fp_crack_v3_handler::fp_crack_v3_handler()
{
}

fp_crack_v3_handler::~fp_crack_v3_handler()
{
}

int fp_crack_v3_handler::process(const fs::http_request& hr,unsigned int ip,string& svid,string& parsestr,string& resp,unsigned int tid)
{
    int res = 0;
    req_struct_t treq;
    string info = hr._req._content;
    string uid;
    string paramstr = hr._req._paramstr;
    res = get_uid(paramstr, uid);
    if (uid.empty()) {
        return -1;
    }
    
    KeyValue result;
    res = check_param(info, uid, result, tid);
    if (res != 0) {
        return -1;
    }
    
    treq._body = info;
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
        if (data.size() <= 0 && configure::instance()->get_slave_switch() == "on")
        {
            slave_mgr::instance()->get_data(skey, data);
        }
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

int fp_crack_v3_handler::response(string& resp, unsigned int tid)
{
    encrypt_t info;
    info.encrypt_str = resp;
    int res = security_mgr::instance()->encrypt_xor(info, tid);
    if (res != 0) {
        return -1;
    }
    resp.clear();
    
    Json::Value value;
    value["a"] = util::instance()->int2str(info.a_index);
    value["b"] = util::instance()->int2str(info.k_index);
    value["c"] = util::instance()->int2str(info.random);
    value["d"] = info.encrypt_str;
    value["e"] = util::instance()->int2str(1);
    
    Json::FastWriter writer;
    resp = writer.write(value);
    
    return 0;
}
