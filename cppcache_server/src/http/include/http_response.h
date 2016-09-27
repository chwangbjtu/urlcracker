#ifndef __HTTP_RESPONSE_H
#define __HTTP_RESPONSE_H
#include "http_def.h"

BEGIN_FS_NAMESPACE

class http_response
{
public:
	http_response(void);
	~http_response(void);
	
	/*
	*	pack the @_resp to the @buff with length @len, use http response format
	*@param buf : data buffer packed to
	*@param len : size of the data buffer, output the pack size
	*return:
	*	0--success, < 0--error occured
	*/
	int pack(char *buf, int &len);

	/*
	*	pack the @_resp to the string buffer @strbuf
	*return:
	*	0--success, other--failed.
	*/
	int pack(string &strbuf, bool b_gzip = false);

	/*
	*	parse http response from @buf which the data length is @len
	*@param buf : data to parse
	*@param len : length of data buffer
	*return:
	*	0--success, < 0--error occured
	*/
	int parse(const char *buf, const int len);

public:

	response_t _resp;
};

END_FS_NAMESPACE
#endif
