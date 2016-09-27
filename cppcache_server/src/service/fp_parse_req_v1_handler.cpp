#include <arpa/inet.h>
#include <netdb.h>
#include "json/json.h"
#include "dbg.h"
#include "client_req_struct.h"
#include "redis_mgr.h"
#include "tlogger.h"
#include "json_converter.h"
#include "fp_parse_req_v1_handler.h"
//#include "util.h"
#include "md5.h"

int fp_parse_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& svid,string& parsestr,string& resp,unsigned int tid)
{
    int res = 0;
    //hr._req._content
    req_struct_t treq;

    string info = hr._req._content;
    treq._body = info;
    Json::Reader reader;
    Json::Value value;
    if ( !reader.parse(info,value) || value.type() != Json::objectValue )
    {
        res = -1;
        return res;
    }

    multimap<string, string>::const_iterator c_iter = hr._req._map_params.find("parsestr");
    if ( c_iter != hr._req._map_params.end())
    {
        parsestr = c_iter->second;
    }

    const string ssvid = "vid";
    string vid;
    //if ( value.isMember("vid") && !value["vid"].isNull()
    //    && value["vid"].isString())
    
    if ( value.isMember(ssvid) && !value[ssvid].isNull()
        && value[ssvid].isString())
    {
        //Json::Value avalue = value["vid"];
        vid = value[ssvid].asString();
    }

    string site;
    const string ssite = "site";
    if ( value.isMember(ssite) && !value[ssite].isNull()
        && value[ssite].isString())
    {
        site = value[ssite].asString();
        
        //测试接口，禁用功能不需要
        //if (0 != util::instance()->check_forbidden(site)) {
        //    return -1;
        //}
    }

    string url;
    const string surl = "url";
    if (value.isMember(surl) && !value[surl].isNull()
        && value[surl].isString())
    {
        url = value[surl].asString();
    }

    if (vid.size() == 0 || site.size() == 0 || url.size() == 0)
    {
        return -1;
    }

    string data;
    //string skey = "crack:"+site+":"+vid;
    string skey = "crack:" + site + ":" + vid + ":" + md5(url.substr(0, url.find("?")));
    if (skey.size() > 0)
    {
        svid = skey;
        redis_mgr::instance()->get_data(skey,data);
    }
    if (data.size() > 0 )
    {
        treq._hit = 1;
        string tdata;
        tdata = json_converter::instance()->convertstr(parsestr,data);
    }
    else
    {
        redis_mgr::instance()->push_list_data(hr._req._content);
        treq._hit = 0;
    }

    treq._vid = skey;
    treq._ip = ip;
    treq._type = 0;
    tlogger::instance()->log(treq);

    /*
	const multimap<string,string> req = hr._req._map_params;

	if ( pack("",resp) < 0)
	{
		return -1;
	}
    */
	return 0;
}

/*
int fp_android_ios_req_v2_handler::unpack(const multimap<string,string>& req,android_req_struct_t& req_struct)
{
	//multimap<string,string>::const_iterator iter = req.find("msgid");

	return 0;
}
*/
