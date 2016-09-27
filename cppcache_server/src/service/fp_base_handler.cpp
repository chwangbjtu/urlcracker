#include <arpa/inet.h>
#include <netdb.h>
#include <vector>
#include "k_str.h"
#include "http_util.h"
#include "http_response.h"
#include "json/json.h"
#include "util.h"
#include "security_mgr.h"
#include <algorithm>
#include "fp_base_handler.h"

using namespace std;

fp_base_handler::fp_base_handler()
{
	//_return_succ = util::instance()->get_return_succ();
}

int fp_base_handler::pack(string& msg,string& resp)
{
	fs::http_response http_resp;
	
	http_resp._resp._content = msg;
	if(http_resp.pack(resp) < 0) 
	{
		return -1;
	}
	return 0;
}

const string& fp_base_handler::find_user_agent(const fs::http_request& hr)
{
    static const string empty;
    multimap<string, string>::const_iterator user_agent_it = hr._req._map_headers.find("User-Agent");

    if(hr._req._map_headers.end() == user_agent_it)
    {
        return empty;
    }

    return user_agent_it->second;
}

const unsigned int fp_base_handler::find_xforwardedfor(const fs::http_request& hr)
{
    /*
	unsigned int ip = 0;
	
	//format : X-Forwarded-For: client1, proxy1, proxy2
	const unsigned int least_addr_num = 1;
	const int client_index = 0;
	
	static const char* x_forwarded_for = "X-FORWARDED-FOR";
	multimap<string,string>::const_iterator forwarded_iter = hr._req._map_headers.begin();
	multimap<string,string>::const_iterator forwarded_iter_end = hr._req._map_headers.end();
	for(; forwarded_iter != forwarded_iter_end; ++forwarded_iter) 
	{
		const string header_keyword = fs::str2upper( forwarded_iter->first );
		if( header_keyword.compare(x_forwarded_for) != 0 )
			continue;

		//DBG_INFO(("%s", forwarded_iter->second.c_str()));
		vector<string> proxy_addr;
		fs::split(forwarded_iter->second,',',proxy_addr);

		if (proxy_addr.size() >= least_addr_num) 
		{
			util::instance()->str2ip(proxy_addr[client_index], ip); 
		}
		break;
	}

	return ip;
    */
    return 0;
}

int fp_base_handler::check_param(string& param, string& uid, KeyValue& result, unsigned int tid)
{
    if (0 != parse_param(param, result)) {
        return -1;
    }
    
    if (0 != util::instance()->check_forbidden(result["site"])) {
        return -1;
    }

    string client_k = result["k"];
    string params;
    params += result["vid"];
    params += result["url"];
    params += result["site"];
    params += result["os"];
    params += uid;
    string result_k = security_mgr::instance()->get_md5(params, tid);
    
    if (client_k.compare(result_k) != 0) {
        return -1;
    }
    return 0;
}

int fp_base_handler::parse_param(string& param, KeyValue& result)
{
    Json::Reader reader;
    Json::Value value;
    if (!reader.parse(param, value) || value.type() != Json::objectValue ) {
        return -1;
    }
    
    if (!value.isMember("k") || !value.isMember("vid") 
        || !value.isMember("site") || !value.isMember("url")
        || !value.isMember("os")) {
        return -1;
    }
    
    Json::Value::Members keys = value.getMemberNames();
    for (size_t i = 0; i < keys.size(); ++i) {
        if (!value[keys[i]].isString()) {
            return -1;
        }
        result.insert(make_pair(keys[i], value[keys[i]].asString()));
    }
    
    return 0;
}

int fp_base_handler::get_uid(string& param, string& uid)
{
    vector <string> params;
    util::instance()->split(param, "&", params);
    for (size_t i = 0; i < params.size(); ++i) {
        vector <string> key_value;
        util::instance()->split(params[i], "=", key_value);
        vector <string>::iterator iter = find(key_value.begin(), key_value.end(), "uid");
        if (iter != key_value.end()) {
            ++iter;
            if (iter != key_value.end()) {
                uid = *iter;
                break;
            }
        }
    }
    return 0;
}

int fp_base_handler::build_task(KeyValue& result, string& task)
{
    Json::Value value;
    value["vid"] = result["vid"];
    value["site"] = result["site"];
    value["url"] = result["url"];
    value["os"] = result["os"];
    
    Json::FastWriter writer;
    task = writer.write(value);
    return 0;
}


