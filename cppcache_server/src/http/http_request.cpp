#include <stdio.h>
#include <string.h>
#include "http_request.h"
#include "http_util.h"
#include "k_str.h"
#include "k_os.h"

BEGIN_FS_NAMESPACE

http_request::http_request(void)
{
}

http_request::~http_request(void)
{
}


int http_request::pack_get(char *buf, const int len)
{
	if(_req._method != "GET")
	{//method must be get!!
		return -1;
	}

	int pos = 0, num = 0;

	//method and path
	num = snprintf(buf+pos, len-pos, "%s %s", _req._method.c_str(), _req._path.c_str());
	if(num < 0)
		return -1;
	pos += num;

	//if there is parameters, add '?' after path
	if(_req._map_params.size() > 0)
	{
		num = snprintf(buf+pos, len-pos, "%s", "?");
		if(num < 0)
			return -1;
		pos += num;
	}

	//parameters
	multimap<string, string>::const_iterator c_iter = _req._map_params.begin();
	multimap<string, string>::const_iterator c_iter_end = _req._map_params.end();
	
	if(c_iter != c_iter_end)
	{
		string key(""), val("");
		str2escape(c_iter->first.c_str(),c_iter->first.length(), key);
		str2escape(c_iter->second.c_str(),c_iter->second.length(), val);

		num = snprintf(buf+pos, len-pos, "%s=%s", key.c_str(), val.c_str());
		if(num < 0)
			return -1;

		pos += num;

		c_iter++;
	}

	for(; c_iter!=c_iter_end; c_iter++)
	{
		string key(""), val("");
		str2escape(c_iter->first.c_str(),c_iter->first.length(), key);
		str2escape(c_iter->second.c_str(),c_iter->second.length(), val);

		num = snprintf(buf+pos, len-pos, "&%s=%s", key.c_str(), val.c_str());
		if(num < 0)
			return -1;
		pos += num;
	}

	//HTTP version
	num = snprintf(buf+pos, len-pos, " HTTP/%s\r\n", _req._version.c_str());
	if(num < 0)
		return -1;
	pos += num;

	//headers
	c_iter = _req._map_headers.begin();
	c_iter_end = _req._map_headers.end();

	for(; c_iter != c_iter_end; c_iter++)
	{
		string key(""), val("");
		str2escape(c_iter->first.c_str(),c_iter->first.length(), key);
		str2escape(c_iter->second.c_str(),c_iter->second.length(), val);

		num = snprintf(buf+pos, len-pos, "%s: %s\r\n", key.c_str(), val.c_str());
		if(num < 0)
			return -1;
		pos += num;
	}

	//do not forget the last "\r\n"
	num = snprintf(buf+pos, len-pos, "%s", "\r\n");
	if(num < 0)
		return -1;
	pos += num;

	return 0;
}

int http_request::parse(const char *buf, const int len)
{
	try
	{
		if(len < MIN_HTTP_LEN)
		{
			cerr<<"error: too small http request header, buf: \n"<<buf<<endl;
			return -1;
		}

		//find first line end separator
		const char *first_line_sep = strstr(buf, SEP_LINE);
		if(first_line_sep == NULL)
		{
			cerr<<"error: missing method, param and http protocol version, buf: \n"<<buf<<endl;
			return -1;
		}

		//find method
		const char *method_sep = (const char *)memchr(buf, SEP_GET, first_line_sep-buf);
		if(method_sep == NULL)
		{
			cerr<<"error: missing method, buf: \n"<<buf<<endl;
			return -1;
		}
		_req._method = string(buf, method_sep-buf);

		if(_req._method == "GET")
		{
			return parse_get(buf,len); 
		}
		else if(_req._method == "POST")
		{
			return parse_post(buf,len);
		}
		else
		{//unsupported method
			cerr<<"error: unsupported method, buf: \n"<<buf<<endl;
			return -1;
		}
	}
	catch (...)
	{
		cerr<<"error: parse http request failed, buf: \n"<<buf<<endl;
		return -1;
	}

	return 0;
}

int http_request::parse_post(const char *buf, const int len)
{
	try
	{
		if(len < MIN_HTTP_LEN)
		{
			cerr<<"error: too small http request header, buf: \n"<<buf<<endl;
			return -1;
		}

		//find first line end separator
		const char *first_line_sep = strstr(buf, SEP_LINE);
		if(first_line_sep == NULL)
		{
			cerr<<"error: missing method, param and http protocol version, buf: \n"<<buf<<endl;
			return -1;
		}

		//find method
		const char *method_sep = (const char *)memchr(buf, SEP_GET, first_line_sep-buf);
		if(method_sep == NULL)
		{
			cerr<<"error: missing method, buf: \n"<<buf<<endl;
			return -1;
		}
		_req._method = string(buf, method_sep-buf);
		if(_req._method != "POST")
		{//unsupported method
			cerr<<"error: unsupported method, buf: \n"<<buf<<endl;
			return -1;
		}

		//find path & parameter
		const char *path_param_sep = (const char *)memchr(method_sep+1, SEP_URL, first_line_sep-method_sep);
		if(path_param_sep == NULL)
		{
			cerr<<"error: missing url and parameter, buf: \n"<<buf<<endl;
			return -1;
		}

		//path and parameters
		_req._path_and_parameters = string(method_sep+1, path_param_sep-method_sep-1);

		const char *path_sep = (const char *)memchr(method_sep+1, SEP_QM, 
													path_param_sep-method_sep);
		if(path_sep == NULL)
		{//no parameters
			_req._path = string(method_sep+1, path_param_sep-method_sep-1);
		}
		else
		{//with parameters
			//path
			_req._path = string(method_sep+1, path_sep-method_sep-1);

			//parameter strings
			_req._paramstr = string(path_sep+1, path_param_sep-path_sep-1);

			//parse parameters
			parse_parameter(path_sep+1, path_param_sep-path_sep-1, _req._map_params);
		}

		//find http version
		const char *version_sep = (const char *)memchr(path_param_sep+1, 
													   SEP_VERSION, 
													   first_line_sep-path_param_sep-1);
		if(version_sep != NULL)
		{
			string httpstr = string(path_param_sep+1, version_sep-path_param_sep-1);
			if(strcasecmp(httpstr.c_str(), "HTTP") == 0)
			{
				_req._version = string(version_sep+1, first_line_sep-version_sep-1);
				if(_req._version != "1.0" && _req._version != "1.1")
				{
					cerr<<"error: unsupported http version, buf: \n"<<buf<<endl;
					return -1;
				}
			}
			else
			{
				cerr<<"error: missing http version, buf: \n"<<buf<<endl;
				return -1;
			}
		}
		else
		{
			cerr<<"error: missing http version, buf: \n"<<buf<<endl;
			return -1;
		}

		//parse header
		const char *pos_header_start = first_line_sep+2;

		//find end position of headers
		const char *pos_header_end = strstr(first_line_sep, HEADER_END);
		if(pos_header_end == NULL)
		{
			cerr<<"error: missing header end tag, buf: \n"<<buf<<endl;
			return -1;
		}

		parse_headers(pos_header_start, 
						pos_header_end-pos_header_start+4, 
						_req._map_headers);

		const char *pos_content_start = pos_header_end + 4;
		const char *pos_content_end = buf+len;

		_req._content = string(pos_content_start,pos_content_end);
	}
	catch (...)
	{
		cerr<<"error: parse http request failed, buf: \n"<<buf<<endl;
		return -1;
	}

	return 0;
}

int http_request::parse_get(const char *buf, const int len)
{
	try
	{
		if(len < MIN_HTTP_LEN)
		{
			cerr<<"error: too small http request header, buf: \n"<<buf<<endl;
			return -1;
		}

		//find first line end separator
		const char *first_line_sep = strstr(buf, SEP_LINE);
		if(first_line_sep == NULL)
		{
			cerr<<"error: missing method, param and http protocol version, buf: \n"<<buf<<endl;
			return -1;
		}

		//find method
		const char *method_sep = (const char *)memchr(buf, SEP_GET, first_line_sep-buf);
		if(method_sep == NULL)
		{
			cerr<<"error: missing method, buf: \n"<<buf<<endl;
			return -1;
		}
		_req._method = string(buf, method_sep-buf);
		if(_req._method != "GET")
		{//unsupported method
			cerr<<"error: unsupported method, buf: \n"<<buf<<endl;
			return -1;
		}

		//find path & parameter
		const char *path_param_sep = (const char *)memchr(method_sep+1, SEP_URL, first_line_sep-method_sep);
		if(path_param_sep == NULL)
		{
			cerr<<"error: missing url and parameter, buf: \n"<<buf<<endl;
			return -1;
		}

		//path and parameters
		_req._path_and_parameters = string(method_sep+1, path_param_sep-method_sep-1);

		const char *path_sep = (const char *)memchr(method_sep+1, SEP_QM, 
													path_param_sep-method_sep);
		if(path_sep == NULL)
		{//no parameters
			_req._path = string(method_sep+1, path_param_sep-method_sep-1);
		}
		else
		{//with parameters
			//path
			_req._path = string(method_sep+1, path_sep-method_sep-1);

			//parameter strings
			_req._paramstr = string(path_sep+1, path_param_sep-path_sep-1);

			//parse parameters
			parse_parameter(path_sep+1, path_param_sep-path_sep-1, _req._map_params);
		}

		//find http version
		const char *version_sep = (const char *)memchr(path_param_sep+1, 
													   SEP_VERSION, 
													   first_line_sep-path_param_sep-1);
		if(version_sep != NULL)
		{
			string httpstr = string(path_param_sep+1, version_sep-path_param_sep-1);
			if(strcasecmp(httpstr.c_str(), "HTTP") == 0)
			{
				_req._version = string(version_sep+1, first_line_sep-version_sep-1);
				if(_req._version != "1.0" && _req._version != "1.1")
				{
					cerr<<"error: unsupported http version, buf: \n"<<buf<<endl;
					return -1;
				}
			}
			else
			{
				cerr<<"error: missing http version, buf: \n"<<buf<<endl;
				return -1;
			}
		}
		else
		{
			cerr<<"error: missing http version, buf: \n"<<buf<<endl;
			return -1;
		}

		//parse header
		const char *pos_header_start = first_line_sep+2;

		//find end position of headers
		const char *pos_header_end = strstr(first_line_sep, HEADER_END);
		if(pos_header_end == NULL)
		{
			cerr<<"error: missing header end tag, buf: \n"<<buf<<endl;
			return -1;
		}

		parse_headers(pos_header_start, 
						pos_header_end-pos_header_start+4, 
						_req._map_headers);
	}
	catch (...)
	{
		cerr<<"error: parse http request failed, buf: \n"<<buf<<endl;
		return -1;
	}

	return 0;
}

int http_request::set_header(const char *key, const char *val)
{
	_req._map_headers.insert(pair<string, string>(string(key), string(val)));

	return 0;
}

int http_request::set_parameter(const char *key, const char *val)
{
	_req._map_params.insert(pair<string, string>(string(key), string(val)));
	return 0;
}
END_FS_NAMESPACE
