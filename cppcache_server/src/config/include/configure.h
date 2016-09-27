#ifndef __CONFIGURE_H
#define __CONFIGURE_H
#include <string>
#include <map>
#include "kmutex.h"
#include "klock.h"

using namespace std;

#define CPPCACHE_SERVER_VERSION "0.1.0.01"

//configure item
class cdata
{
public:
	cdata():
	_service_port(8080),
	_service_worker_num(4),
	_http_timeout(20),
	_log_buf_size(1024*50),
	_cutdown_interval(300)
	{
		_log_path = "./log/";
		_cppcache_server_ip = "127.0.0.1";
	}

	unsigned short _service_port;
	int _service_worker_num;
	int _http_timeout;
	int _log_buf_size;
	int _cutdown_interval;
	string _log_path;
	string _cppcache_server_ip;
	string _redis_ip;
	int _redis_port;
	string _redis_pwd;
	string _slave_ip;
	int _slave_port;
	string _slave_pwd;
	int _slave_num;
	string _slave_switch;
	string _forbidden_switch;
	string _forbidden_sites;
	string _crack_switch;
	string _cache_switch;
};


/*
 *read configure at  10s interval and check each item.if error found,exit this
 * programme.
 * */
class configure
{
public:
	~configure();
	static configure* instance();
	/* read configure file
	 *@para[in]file:filename of configure name
	 *@return:
	 *  0:success,-1:failed
	 **/
	int start(const string& file);

	int reload();

	//getter 
	unsigned short get_service_port() ;

	int get_service_worker_num();

	int get_http_timeout();

	int get_queue_num();

	string get_log_path();

	int print();

	int get_log_buf_size();

	string get_server_ip();

	string get_server_version();

    string get_redis_ip();

    int get_redis_port();

    string get_redis_pwd();

    string get_slave_ip();

    int get_slave_port();

    string get_slave_pwd();

    int get_slave_num();

    string get_slave_switch();

    string get_forbidden_switch();

    string get_forbidden_sites();

    string get_crack_switch();
    string get_cache_switch();
private:
	configure();
	/* check the  validity of each item in configure file
	 * @para[in]d: configure file item 
	 * @return:
	 *  0:success,-1: error item existed in configure file
	 * */
	int check_config(const cdata& data);
	
	int str2ip(const string& str,unsigned int& ip);
private:
	string _path;
	cdata _data;
	static configure* _inst;
	fsk::kshared_mutex _mutex;
};

#endif//__CONFIGURE_H

