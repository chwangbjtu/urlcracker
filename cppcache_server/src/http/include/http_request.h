#ifndef __HTTP_REQUEST_H
#define __HTTP_REQUEST_H
#include "http_def.h"

BEGIN_FS_NAMESPACE

class http_request
{
public:
	http_request(void);
	~http_request(void);

	/*
	*	parse http request from @buf which the data length is @len
	*@param buf : data to parse
	*@param len : length of data buffer
	*return:
	*	0--success, < 0--error occured
	*/
	int parse(const char *buf,const int len);

	/*
	*	parse http post request from @buf which the data length is @len
	*@param buf : data to parse
	*@param len : length of data buffer
	*return:
	*	0--success, < 0--error occured
	*/
	int parse_post(const char *buf, const int len);

	/*
	*	pack the @_req to the @buff with length @len, use http get request format
	*@param buf : data buffer packed to
	*@param len : size of the data buffer
	*return:
	*	0--success, < 0--error occured
	*/
	int pack_get(char *buf, const int len);

	/*
	*	parse http get request from @buf which the data length is @len
	*@param buf : data to parse
	*@param len : length of data buffer
	*return:
	*	0--success, < 0--error occured
	*/
	int parse_get(const char *buf, const int len);


	/*
	*	add a header item to the request
	*@param key : key of the header, must follow the definition in the http protocol
	*@param val : value of the key, must follow the definition in the http protocol
	*return:
	*	0--success, < 0--error
	*/
	int set_header(const char *key, const char *val);

	/*
	*	add a parameter item to the request
	*@param key : key of the parameter
	*@param val : value of the key
	*return:
	*	0--success, < 0--error
	*/
	int set_parameter(const char *key, const char *val);

public:

	//request data
	request_t _req;
};

END_FS_NAMESPACE

#endif
