#ifndef __UTIL_H
#define __UTIL_H

#include <iostream>
#include "stdint.h"

using namespace std;

class util
{
public:
	~util(){}
	
	static util* instance();
    int64_t get_current_time();
	string get_error_resp();
	int escape2str(const char * str, int len, string &res);
	int ip2str(const unsigned int & ip,string& ipstr);
	int str2ip(const string& str,unsigned int& ip); 
    void split(string& src, const string& delim, vector<string >& ret); 
    int add_retmsg(string& param);
    string int2str(int src);
    string int2str(unsigned int src);
    int check_forbidden(const string& site);
	
private:
	util();
	static util* _inst;
	char * HEX_STR;
    string _err_resp;
};

#endif//__UTIL_H



