#ifndef __HTTP_UTIL_H
#define __HTTP_UTIL_H
#include <string>
#include <vector>
#include <map>
#include <iostream>
#include "k_ns.h"

BEGIN_FS_NAMESPACE

using namespace std;

int escape2llstr(const char * str, int len, string &res);

//split string by separator
int split(const string &str, const char sep, vector<string> &elements);

//parse a host or ip address from a url like: http://xxx.xxx.xxx:port/xxx?xxx=xxx&...
int parse_address(const string &url, string &host, unsigned short &port);

//parse http get parameter from a string like: key1=value1&key2=value2&...
int parse_parameter(const char *param_str, int len, multimap<string, string> &param_pairs);

//parse http get headers
int parse_headers(const char *header_str, int len, multimap<string, string> &header_pairs);

END_FS_NAMESPACE
#endif
