#include <arpa/inet.h>
#include <netdb.h>
#include <iostream>
#include "dbg.h"
#include "json/json.h"
#include "util.h"
#include "configure.h"
#include <string.h>
#include <sys/time.h>

using namespace std;

util* util::_inst = NULL;
util* util::instance()
{
	if ( _inst == NULL)
		_inst = new util();
	return _inst;
}

util::util()
{
    Json::Value tmp_value;
    tmp_value["retcode"] = "404";
    tmp_value["retmsg"] = "crack failed";
    Json::FastWriter writer;
    _err_resp = writer.write(tmp_value);
}

int64_t util::get_current_time()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (int64_t)(tv.tv_sec * 1000 + tv.tv_usec / 1000);
}

string util::get_error_resp()
{
    //DBG_INFO("info _err_resp: %x", _err_resp.c_str());
    return _err_resp;
}

int util::ip2str(const unsigned int & ip,string& ipstr)
{
	struct in_addr ip_addr;
	memset(&ip_addr,0,sizeof(in_addr));
	ip_addr.s_addr = ip;
	char ipbuf[INET_ADDRSTRLEN]= {0};
	if ( inet_ntop(AF_INET,(struct in_addr*)&ip_addr,ipbuf,INET_ADDRSTRLEN)!= NULL) 
	{
		ipstr = string(ipbuf,strlen(ipbuf));
		return 0;
	}
	return -1;
}

int util::str2ip(const string& str,unsigned int& ip)
{
	in_addr ipaddr;
	memset(&ipaddr,0,sizeof(ipaddr));
	if ( inet_pton(AF_INET,str.c_str(),(struct in_addr*)&ipaddr) > 0) 
	{
		ip = ntohl(ipaddr.s_addr);
		return 0;
	}
	return -1;
}


/*
*	decode escape string (like %AB%0D%....) to strings
*@param str	input string to decode
*@param len	length of the str
*@res	out, decode result
*return:
*	0, always success
*/
int util::escape2str(const char * str, int len, string &res)
{
	int i=0;
	int pos = 0;
	char buf[65535] = {0};
	while(i < len)
	{
		char c = *(str+i);
		if(c != '%')
		{
			*(buf+pos) = c;
			pos++;
			i++;
		}
		else
		{
			if(i < len-2)
			{
				i++;
				c = *(str+i);

				if(c>='0' && c<='9')
					*(buf+pos) |= ((c-'0')<<4);
				else if(c>='a' && c<='f')
					*(buf+pos) |= ((c-'a'+10)<<4);
				else if(c>='A' && c<='F')
					*(buf+pos) |= ((c-'A'+10)<<4);
				else
					break;

				i++;
				c = *(str+i);
				if(c>='0' && c<='9')
					*(buf+pos) |= ((c-'0'));
				else if(c>='a' && c<='f')
					*(buf+pos) |= ((c-'a'+10));
				else if(c>='A' && c<='F')
					*(buf+pos) |= ((c-'A'+10));
				else
					break;

				pos++;
				i++;
			}
			else
				break;
		}
	}

	res.assign(buf, pos);
	return 0;
}

void util::split(string& src, const string& delim, vector<string >& ret)
{
    size_t last = 0;
    size_t index = src.find_first_of(delim, last);
    while (index != string::npos)
    {
        ret.push_back(src.substr(last, index - last));
        last = index + 1;
        index = src.find_first_of(delim, last);
    }
    if (index - last > 0)
    {
        ret.push_back(src.substr(last, index - last));
    }
}

int util::add_retmsg(string& param)
{
    Json::Reader reader;
    Json::Value value;
    if (!reader.parse(param, value) || value.type() != Json::objectValue ) {
        return -1;
    }
    
    if (!value.isMember("retcode") || !value.isMember("retmsg")) {
        value["retcode"] = "200";
        value["retmsg"] = "ok";
    }

    param.clear();
    Json::FastWriter writer;
    param = writer.write(value);
    return 0;
}

string util::int2str(int src)
{
    string dest;
    dest.resize(64, 0);
    
    sprintf(&dest[0], "%d", src);
    return dest;
}

string util::int2str(unsigned int src)
{
    string dest;
    dest.resize(64, 0);
    
    sprintf(&dest[0], "%u", src);
    return dest;
}

int util::check_forbidden(const string& site)
{
    if ( site.empty() )
    {
        return 0;
    }
    //检测是否禁用
    string forbidden_switch  = configure::instance()->get_forbidden_switch();
    if ( forbidden_switch == "on")
    {
        string forbidden_sites  = configure::instance()->get_forbidden_sites();
        if ( !forbidden_sites.empty() )
        {
            vector<string> split_sites;
            util::instance()->split(forbidden_sites, ";", split_sites);
            for(int i=0; i < split_sites.size(); i++)
            {
                if (site == split_sites[i])
                {
                    return -1;
                }
            }
        }
    }
    return 0;
}

