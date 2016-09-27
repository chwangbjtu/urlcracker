#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "k_os.h"
#include "compress.h"
#include "http_response.h"
#include "http_util.h"

BEGIN_FS_NAMESPACE

http_response::http_response(void)
{
}

http_response::~http_response(void)
{
}

int http_response::pack(char *buf, int &len)
{
	int pos = 0, num = 0;

	//http version, code, code information
	num = snprintf(buf+pos, len-pos, "HTTP/%s %s %s\r\n", 
					_resp._version.c_str(), 
					_resp._code.c_str(), 
					_resp._code_info.c_str());
	if(num < 0)
		return -1;
	pos += num;

	kt::u_long content_len = _resp._content.length();
	//the content is empty
	if(content_len == 0)
	{//no content
		const char *default_header = "Content-Length: 0\r\n"
									 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
									 "Cache-Control: no-cache, must-revalidate\r\n"
									 "Pragma: no-cache\r\n"
									 "Content-type: text/plain\r\n"
									 "Connection: Close\r\n\r\n";

		num = snprintf(buf+pos, len-pos, default_header);
		if(num < 0)
			return -1;
		pos += num;
		
		len = pos;

		return 0; //work is down, return
	}

	//gzip the content
	kt::u_long buf_len = content_len+64;
	char *content_buf = new char[buf_len];
	int zip_res = gzip((u_char*)content_buf, 
						&buf_len, 
						(u_char*)_resp._content.c_str(), 
						content_len);

	if(zip_res != Z_OK)
	{//zip failed, use original content
		//free the content zip buffer first
		delete content_buf;

		const char *default_header = "Content-Length: %d\r\n"
									 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
									 "Cache-Control: no-cache, must-revalidate\r\n"
									 "Pragma: no-cache\r\n"
									 "Content-type: text/plain\r\n"
									  "Connection: Close\r\n\r\n";

		num = snprintf(buf+pos, len-pos, default_header, content_len);
		if(num < 0)
			return -1;
		pos += num;

		//content
		memcpy(buf+pos, _resp._content.c_str(), content_len);
		pos += content_len;
		len = pos;
	}
	else
	{//use zipped content
		const char *default_header = "Content-Encoding: gzip, deflate\r\n"
									 "Content-Length: %d\r\n"
									 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
									 "Cache-Control: no-cache, must-revalidate\r\n"
									 "Pragma: no-cache\r\n"
									 "Content-type: text/plain\r\n"
									 "Connection: Close\r\n\r\n";
		num = snprintf(buf+pos, len-pos, default_header, buf_len);
		if(num < 0)
		{
			delete content_buf;
			return -1;
		}
		pos += num;	

		//content
		memcpy(buf+pos, content_buf, buf_len);
		pos += content_len;
		len = pos;

		delete content_buf;
	}

	return 0;
}

int http_response::pack(string &strbuf, bool b_gzip)
{
	strbuf = "";
	/*initial temporary buffer*/
	const int len = 1024*10;
	char buf[len] = {0};

	//http version, code, code information
	int num = snprintf(buf, len, "HTTP/%s %s %s\r\n", _resp._version.c_str(), 
					_resp._code.c_str(), _resp._code_info.c_str());
	if(num < 0)
		return -1;

	strbuf.append(buf, num);

	kt::u_long content_len = _resp._content.length();
	//the content is empty
	if(content_len == 0)
	{//no content
		const char *default_header = "Content-Length: 0\r\n"
									 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
									 "Cache-Control: no-cache, must-revalidate\r\n"
									 "Pragma: no-cache\r\n"
									 "Content-type: text/plain\r\n"
									 "Connection: Close\r\n\r\n";

		num = snprintf(buf, len, default_header);
		if(num < 0)
			return -1;
		strbuf.append(buf, num);
		return 0; //work is down, return
	}

	if(b_gzip)
	{
		//gzip the content
		kt::u_long buf_len = content_len+64;
		char *content_buf = new char[buf_len];
		int zip_res = gzip((u_char*)content_buf, 
							&buf_len, 
							(u_char*)_resp._content.c_str(), 
							content_len);

		if(zip_res != Z_OK)
		{//zip failed, use original content
			//free the content zip buffer first
			delete content_buf;

			const char *default_header = "Content-Length: %d\r\n"
										 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
										 "Cache-Control: no-cache, must-revalidate\r\n"
									     "Pragma: no-cache\r\n"
									     "Content-type: text/plain\r\n"
										"Connection: Close\r\n\r\n";

			num = snprintf(buf, len, default_header, content_len);
			if(num < 0)
				return -1;
			strbuf.append(buf, num);
			strbuf.append(_resp._content);
		}
		else
		{//use zipped content
			const char *default_header = "Content-Encoding: gzip, deflate\r\n"
										 "Content-Length: %d\r\n"
										 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
										 "Cache-Control: no-cache, must-revalidate\r\n"
										 "Pragma: no-cache\r\n"
										 "Content-type: text/plain\r\n"
										"Connection: Close\r\n\r\n";
			num = snprintf(buf, len, default_header, buf_len);
			if(num < 0)
			{
				delete content_buf;
				return -1;
			}
			strbuf.append(buf, num);
			strbuf.append(content_buf, buf_len);
			delete content_buf;
		}
	}
	else
	{
		const char *default_header = "Content-Length: %d\r\n"
									 "Expires: Mon, 26 Jul 1997 05:00:00 GMT\r\n"
									 "Cache-Control: no-cache, must-revalidate\r\n"
									 "Pragma: no-cache\r\n"
									 "Content-type: text/plain\r\n"
									"Connection: Close\r\n\r\n";

		num = snprintf(buf, len, default_header, content_len);
		if(num < 0)
			return -1;
		strbuf.append(buf, num);
		strbuf.append(_resp._content);
	}
	return 0;
}

int http_response::parse(const char *buf, const int len)
{
	const char *pos_header_end = strstr(buf, "\r\n\r\n");
	if(pos_header_end == NULL)
	{//can not find header end separator, error package
		cerr<<"error: can not find http response header end separator, buf: \n"<<buf<<endl;
		return -1;
	}

	//find first line end separator
	const char *first_line_sep = strstr(buf, SEP_LINE);
	if(first_line_sep == NULL)
	{
		cerr<<"error: missing http protocol version, response code and information, buf: \n"<<buf<<endl;
		return -1;
	}

	//find http protocol version
	const char *pos_protocol_end = (const char *)memchr(buf, SEP_SPACE, first_line_sep-buf);
	if(pos_protocol_end == NULL)
	{
		cerr<<"error: missing http protocol version, buf: \n"<<buf<<endl;
		return -1;
	}
	const char *pos_version_sep = (const char *)memchr(buf, SEP_VERSION, pos_protocol_end-buf);
	if(pos_version_sep != NULL)
	{
		string httpstr = string(buf, pos_version_sep-buf);
		if(strcasecmp(httpstr.c_str(), "HTTP") == 0)
		{
			_resp._version = string(pos_version_sep+1, pos_protocol_end-pos_version_sep-1);
			if(_resp._version != "1.0" && _resp._version != "1.1")
			{
				cerr<<"error: unsupported http version, buf: \n"<<buf<<endl;
				return -1;
			}
		}
		else
		{
			cerr<<"error: missing http protocol version, buf: \n"<<buf<<endl;
			return -1;
		}
	}
	else
	{
		cerr<<"error: missing http protocol version, buf: \n"<<buf<<endl;
		return -1;
	}

	//find response code
	const char *pos_code_end = (const char *)memchr(pos_protocol_end+1, SEP_SPACE, first_line_sep-pos_protocol_end-1);
	if(pos_code_end == NULL)
	{
		cerr<<"error: missing response code, buf: \n"<<buf<<endl;
		return -1;
	}
	_resp._code = string(pos_protocol_end+1, pos_code_end-pos_protocol_end-1);

	//find response info
	_resp._code_info = string(pos_code_end+1, first_line_sep-pos_code_end-1);

	//parse response headers
	parse_headers(first_line_sep+2, 
				(int)(pos_header_end-first_line_sep+2), 
				_resp._map_headers);

	//content start pointer and length
	const char *p_content = pos_header_end+4;
	kt::u_long content_len = (kt::u_long)(len-(pos_header_end-buf+4));

	//check the content length
	multimap<string, string>::const_iterator c_iter;
	c_iter = _resp._map_headers.find("Content-Length");
	if(c_iter != _resp._map_headers.end())
	{
		kt::u_long len = atol(c_iter->second.c_str());
		if(len != content_len)
		{//content length is not match the actual size
			return -1;
		}
	}

	//find Content-Encoding
	c_iter = _resp._map_headers.find("Content-Encoding");
	if(c_iter != _resp._map_headers.end())
	{
		if((strstr(c_iter->second.c_str(), "gzip") != NULL 
			|| strstr(c_iter->second.c_str(), "deflate") != NULL) 
			&& content_len > 0)
		{//decompress the content
			//first 3 times of the zipped data size
			kt::u_long buf_len = 3*content_len;
			kt::byte *content_buf = new kt::byte[buf_len];

			int zip_res = un_gzip(content_buf, &buf_len, (u_char*)p_content, content_len);
			while(zip_res == Z_BUF_ERROR)
			{//buffer is too small for unzip the compressed content
				buf_len += content_len; //increase the content buffer length by content_len
				content_buf = (u_char*)realloc(content_buf, buf_len);
				int zip_res = un_gzip(content_buf, 
									  &buf_len, 
									  (u_char*)p_content, 
									  content_len);
			}
			
			if(zip_res == Z_OK)
			{
				delete content_buf; //do not forget free the buffer
				_resp._content = string((char*)content_buf, buf_len);
			}
			else
			{
				delete content_buf; //do not forget free the buffer
				return -1;
			}
		}
		else //unsupported content encoding
			return -1;
	}
	else //content is not zipped
		_resp._content = string(p_content, content_len);

	return 0;
}
END_FS_NAMESPACE
