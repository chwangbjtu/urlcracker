#include <sys/time.h>
#include "k_str.h"
#include "tcp_netio.h"
#include "dbg.h"
#include "util.h"
#include "redis_mgr.h"
#include "proto_dispatcher.h"
#include "http_response.h"
#include "configure.h"
#include "client_req_struct.h"
#include "tlogger.h"
#include "json_converter.h"

tcp_netio::tcp_netio():
	_snd_len(0),
	//_ctime(time(NULL)),
	_proto_len(0),
	_content_length(-1),
	_header_length(0)
{
    struct timeval tv;
    gettimeofday(&tv,NULL);
    _ctime = tv.tv_sec * 1000 + tv.tv_usec/1000;
	_timeout = configure::instance()->get_http_timeout();
}

tcp_netio::~tcp_netio()
{
}
int tcp_netio::handle_recv()
{
	const int BUF_LEN = 2048;
	char buf[BUF_LEN] = {0};
	ssize_t recv_len = 0;
	while((recv_len = ::recv(sock(), buf, BUF_LEN, 0)) > 0) 
	{
		_request.append(buf, recv_len);
	}
	if(recv_len < 0 && (errno != EAGAIN && errno != EWOULDBLOCK)) 
	{
		return -1;
	} 
	else if(recv_len == 0 && _request.empty()) 
	{
		return -1;
	}

	string tmp_request;
	//fs::escape2str(_request.data(),_request.size(),tmp_request);
	if ( _request.size() >= 65535)//max packet len
	{
		DBG_ERROR("packet len is over 65535");
		return -1;
	}
	tmp_request = _request;
	
	const char* data = tmp_request.data();
	//if ( tmp_request.find("\r\n\r\n") != string::npos) 
	if ( recv_finished())
	{
		if(proto_dispatcher::instance()->process(tmp_request, peer_ip() ,_vid,_parsestr,_response,thread_index()) < 0) 
		{
			return -1;//close socket
		} 
		else
		{
            if (_response.length() > 0) {
                if(util::instance()->add_retmsg(_response) != 0) {
                    return -1;
                }
                proto_dispatcher::instance()->response(tmp_request, _response, thread_index());
                fs::http_response http_resp;
                http_resp._resp._content = _response;
                if(http_resp.pack(_response) < 0)
                {
                    return -1;
                }
            }
			return handle_send();
		}
	} 
	else
	{
		return 0;//continue to receive
	}
	return -1;
}

int tcp_netio::handle_open(void *arg)
{
	return 0;
}

int tcp_netio::handle_send()
{
	if(_response.length() == 0) 
	{
		return 0;
	}
	size_t resp_len = _response.length();
	while (_snd_len < resp_len) 
	{
		ssize_t n = ::send(sock(), _response.data()+_snd_len,resp_len-_snd_len, 0);
		if(n > 0)
		{
			_snd_len += (size_t)n;
		}
		else if(n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK ))
		{
			/* action blocked */
			return 0;
		}
		else 
		{
			break;
		}
	}
	//send all response
	_response.clear();
	return -1;
}
int tcp_netio::handle_close()
{
	return -1;
}

int tcp_netio::handle_run(time_t t)
{
	//if((t - _ctime) > _timeout) 
    struct timeval tv;
    gettimeofday(&tv,NULL);
    unsigned long long tnow = tv.tv_sec * 1000 + tv.tv_usec/1000;
    if (tnow - _ctime > _timeout)
	{
        _data = util::instance()->get_error_resp();
        //DBG_INFO("_data: %x", _data.c_str());
		//return -1;
        req_struct_t treq;
        treq._vid = _vid;
        treq._time_out = 1;
        treq._type = 1;
        tlogger::instance()->log(treq);
	}
    else
    {
        redis_mgr::instance()->get_data(_vid,_data);
        if ( _data.size() > 0)
        {
            req_struct_t treq;
            treq._vid = _vid;
            treq._time_out = 0;
            treq._hit = 0;
            treq._parse_over = 1;
            treq._type = 2;
            tlogger::instance()->log(treq);
        }
    }

    if (_data.size() > 0 )
    {
        fs::http_response http_resp;
        string tdata;
        string temp;
        tdata = json_converter::instance()->convertstr(_parsestr,_data);

        if (tdata.length() > 0) {
            //string is Shallow copy, incase of 
            temp.resize(tdata.length(), 0);
            memcpy(&temp[0], &tdata[0], tdata.length());
            if(util::instance()->add_retmsg(temp) != 0) {
                return -1;
            }
            proto_dispatcher::instance()->response(_request, temp, thread_index());
			string cache_switch  = configure::instance()->get_cache_switch();
			if (cache_switch == "on")
			{
				redis_mgr::instance()->del_data(_vid);
			}
        }
        http_resp._resp._content = temp;
        if(http_resp.pack(_response) < 0)
        {
            return -1;
        }
        
        return handle_send();
    }
	return 0;
}

bool tcp_netio::recv_finished()
{
	if ( _request.compare(0, 4, "GET ", 4) == 0)
	{
		return get_finished();
	} 
	else if (_request.compare(0, 5, "POST ", 5) == 0) 
	{
		return post_finished();
	} 
	else
	{
		return false;
	}
}

int tcp_netio::extract_between(const std::string& data, std::string& result, const std::string& separator1, const std::string& separator2)
{
	std::string::size_type start, limit;

	start = data.find(separator1, 0);

	if ( std::string::npos != start)
	{
		start += separator1.length();
		limit = data.find(separator2, start);
		if ( std::string::npos != limit)
		{
			result = data.substr(start, limit - start);
			return 0;
		} 

	}
	return -1;
}

bool tcp_netio::post_finished()
{
	if ( _content_length <0)
	{
		std::string::size_type pos; 
		pos = _request.find("\r\n\r\n",0);
		if (string::npos == pos )
		{
			return false;
		}
		_header_length = pos +4;
		std::string content_len_str; 
		int ret = 0;
        /*
		string content_lenth = "Content-Length: ";
		ret = extract_between(_request, content_len_str, content_lenth);//in this service http-post-header must have Content-Length:
		if ( ret < 0 )
		{
            return false;
  		} 
        */
        ///
        string content_lenth = "Content-Length: ";
        string content_lenth1 = "Content-length: ";
        string content_lenth2 = "content-length: ";
        string content_lenth3 = "content-Length: ";
        ret = extract_between(_request, content_len_str, content_lenth1);
        if (ret < 0)
        {
           ret = extract_between(_request, content_len_str, content_lenth); 
           if ( ret < 0)
           {
               ret = extract_between(_request, content_len_str, content_lenth2);
               if ( ret < 0)
               {
                   ret = extract_between(_request, content_len_str, content_lenth3);
               }
           }
        }
        if (ret < 0)
        {
            return false;
        }
        ///
		if (is_digit(content_len_str) <0) 
		{
			return false;
		}
		_content_length = atoi(content_len_str.c_str());
         }

	if ( (_content_length + _header_length ) > _request.length())
	{
		return false;
	} 
	return true;
}

bool tcp_netio::get_finished()
{
	std::string::size_type pos; 
	pos = _request.rfind("\r\n\r\n");
	if (string::npos == pos ) 
	{
		return false;
	} 
	else 
	{
		return true;
	}
}

int tcp_netio::is_digit(const string & str)
{
	int size = str.length();
	if ( size == 0)
	{
		return -1;
	}
	
	const char DIGIT_MAX = '9';
	const char DIGIT_MIN = '0';
	int i = 0;
	int ret = 0;
	
	while ( i < size )
	{
		if ( str[i] <= DIGIT_MAX && str[i] >= DIGIT_MIN )
		{
			i++;
			continue;
		}
		else 
		{
			ret = -1;
			break;
		}
	}

	return ret;
}




