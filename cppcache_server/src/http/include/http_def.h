#ifndef __HTTP_CONSTANT_H
#define __HTTP_CONSTANT_H
#include <string>
#include <map>
#include <iostream>
#include "k_ns.h"

BEGIN_FS_NAMESPACE

using namespace std;

/*data type to save http request parse results*/
struct request_t
{
	request_t();
	~request_t();
	//http request method
	string _method;
	//http request path and parameter
	string _path_and_parameters;
	//request path
	string _path;
	//parameters string
	string _paramstr;
	//http version
	string _version;
	//http post information
	string _content;

	//request parameters
	multimap<string, string> _map_params;
	//request headers
	multimap<string, string> _map_headers;
	//request cookies, !!current not used!!
	multimap<string, string> _map_cookies;
};

/*data type to save http response results*/
struct response_t 
{
	response_t();
	~response_t();
	//http version
	string _version;
	//response code
	string _code;
	//response code info
	string _code_info;
	//response header parameters
	multimap<string, string> _map_headers;
	//response content
	string _content;
};

//response encode types
typedef enum encode_type
{
	NONE = 0,
	GZIP = 1,
	DEFLATE = 2
}encode_type;

#define SEP_LINE				"\r\n"
#define HEADER_END				"\r\n\r\n"
#define SEP_GET					' '
#define SEP_URL					' '
#define SEP_SPACE				' '
#define SEP_QM					'?'
#define SEP_EQ					'='
#define SEP_AND					'&'
#define SEP_VERSION				'/'
#define SEP_HEADER				':'
#define MIN_HTTP_LEN				18 //"GET / HTTP/1.1\r\n\r\n"

END_FS_NAMESPACE

#endif
