#ifndef __CLIENT_REQ_STRUCT_H
#define __CLIENT_REQ_STRUCT_H

#include <string>

using namespace std;

class req_struct_t
{
public:
    req_struct_t()
    {
        _hit = 0;
        _time_out = 0;
        _ip = 0;
        _parse_over = 0;
        _type = 0;
    }
	string _vid;
	int _hit;
	int _time_out;
	unsigned int _ip;
    int _parse_over;
    int _type;
    string _body;
};

/*
typedef struct android_req_struct
{
	string _cli;
	string _ps;
	string _mac;
	string _version;
	string _sid;
	string _msg_id;
	string _ip;
}android_req_struct_t;

typedef struct ios_regist_struct
{
	string _device_id;//mac
	string _device_token;
	string _os_type;
	string _sys_ver;
	string _hard_ware_info;
	string _cli_version;
	string _ip;
	string _fudid;
}ios_regist_struct_t;
*/
#endif//__CLIENT_REQ_STRUCT_H


