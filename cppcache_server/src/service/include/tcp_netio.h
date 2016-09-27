#ifndef __HTTP_NETIO_H
#define __HTTP_NETIO_H
#include <string>
#include "tcp_service.h"
using namespace std;

class tcp_netio :public netsvc::epoll_handler
{
public:
	tcp_netio();
	virtual ~tcp_netio(void);
	virtual int handle_open(void *arg);
	virtual int handle_send();
	virtual int handle_recv();
	virtual int handle_close();

	virtual int handle_run(time_t tm);
private:
	bool recv_finished();

	int extract_between(const std::string& data, std::string& result, const std::string& separator1, const std::string& separator2= "\r\n");

	bool post_finished();

	bool get_finished();

	int is_digit(const string & str);

private:
	string		_request;
	string		_response;
    string      _vid;
    string      _data;
    string      _parsestr;
	size_t		_snd_len;
	//time_t		_ctime;
    unsigned long long   _ctime;
	size_t		_proto_len;
	int 			_timeout;
	int 			_content_length;
	int			_header_length;
};

#endif //__HTTP_NETIO_H

