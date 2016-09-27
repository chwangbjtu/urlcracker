#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <math.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <iostream>
#include <sstream>
#include "k_configure.h"
#include "dbg.h"
#include "configure.h"
using  fs::k_configure;

configure* configure::_inst = NULL;

configure::configure()
{
}
configure::~configure() {}

configure* configure::instance()
{
	if ( _inst == NULL)
		_inst = new configure();
	return _inst;
}


int configure::start(const string& path)
{
	//read configure file
	k_configure conf;
	if ( conf.open(path.c_str()) != 0) 
	{
		DBG_ERROR("open configure file error");
		return -1;
	}

	cdata data;

	//service
	int port = 0;
	conf.get_integer_value("service","service_port",port);
    data._service_port = port;
	conf.get_integer_value("service","service_worker_num",data._service_worker_num);
	conf.get_integer_value("service","http_timeout",data._http_timeout);

	//log
	conf.get_string_value("log","log_path",data._log_path);
	conf.get_string_value("log","cppcache_server_ip",data._cppcache_server_ip);
	conf.get_integer_value("log","cutdown_interval",data._cutdown_interval);

    //redis
    conf.get_string_value("redis","redis_ip",data._redis_ip);
    conf.get_integer_value("redis","redis_port",data._redis_port);
    conf.get_string_value("redis","redis_pwd",data._redis_pwd);
    conf.get_string_value("redis","slave_ip",data._slave_ip);
    conf.get_integer_value("redis","slave_port",data._slave_port);
    conf.get_string_value("redis","slave_pwd",data._slave_pwd);
    conf.get_integer_value("redis","slave_num",data._slave_num);
    conf.get_string_value("redis","slave_switch",data._slave_switch);
        
    //switch
    string forbidden_switch = "off";
    conf.get_string_value("switch","forbidden_switch",forbidden_switch);
    data._forbidden_switch = forbidden_switch;
    string forbidden_sites = "";
    conf.get_string_value("switch","forbidden_sites",forbidden_sites);
    data._forbidden_sites = forbidden_sites;
    string crack_switch = "off";
    conf.get_string_value("switch","crack_switch",crack_switch);
    data._crack_switch = crack_switch;
    string cache_switch = "off";
    conf.get_string_value("switch","cache_switch",cache_switch);
    data._cache_switch = cache_switch;

	//check the configure item 
	if ( check_config(data) != 0) 
	{
		DBG_ERROR("check_config() error");
		return -1;
	}

	
	fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
	_path = path;
	_data = data;

	print();

	DBG_INFO("success to read configure");
	return 0;
}

int configure::check_config(const cdata& data)
{
	if(
	      data._service_port <= 0
	   || data._service_worker_num <= 0
	   || data._http_timeout <= 0
	   || data._log_path.size() <= 0
       || data._redis_ip.size() <= 0
       || data._redis_port <= 0
	   || data._cppcache_server_ip.size() <= 0
	   ) 
	{
		DBG_ERROR("configure error may be some parameters <= 0");
		return -1;
	}
	return 0;
}

unsigned short configure::get_service_port() 
{	
	fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._service_port;
}

int configure::get_service_worker_num() 
{	
	fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._service_worker_num;
}

int configure::get_http_timeout()
{
	fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._http_timeout;
}

string configure::get_log_path()
{
	fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._log_path;
}

int configure::get_log_buf_size()
{
	fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._log_buf_size;
}

string configure::get_server_ip()
{
	fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._cppcache_server_ip;
}

string configure::get_server_version()
{
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return CPPCACHE_SERVER_VERSION;
}

string configure::get_redis_ip()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._redis_ip;
}

int configure::get_redis_port()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._redis_port;
}

string configure::get_redis_pwd()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._redis_pwd;
} 

string configure::get_slave_ip()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._slave_ip;
} 

int configure::get_slave_port()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._slave_port;
} 

string configure::get_slave_pwd()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._slave_pwd;
} 

int configure::get_slave_num()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._slave_num;
} 

string configure::get_slave_switch()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._slave_switch;
} 

string configure::get_forbidden_switch()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._forbidden_switch;
}

string configure::get_forbidden_sites()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._forbidden_sites;
}
string configure::get_crack_switch()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._crack_switch;
}
string configure::get_cache_switch()
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._cache_switch;
}

int configure::print()
{
	cout<<"\n=========================configure file=========================\n";
	cout<<"service_port="<<_data._service_port<<endl;
	cout<<"service_worker_num="<<_data._service_worker_num<<endl;
	cout<<"http_timeout="<<_data._http_timeout<<endl;
	cout<<"log_path="<<_data._log_path.data()<<endl;
	cout<<"cppcache_server_ip="<<_data._cppcache_server_ip.data()<<endl;
	cout<<"redis_ip="<<_data._redis_ip<<endl;
	cout<<"redis_port="<<_data._redis_port<<endl;
	cout<<"redis_pwd="<<_data._redis_pwd.data()<<endl;
	cout<<"slave_ip="<<_data._slave_ip<<endl;
	cout<<"slave_port="<<_data._slave_port<<endl;
	cout<<"slave_pwd="<<_data._slave_pwd.data()<<endl;
	cout<<"slave_num="<<_data._slave_num<<endl;
	cout<<"slave_switch="<<_data._slave_switch.data()<<endl;
	cout<<"forbidden_switch="<<_data._forbidden_switch.data()<<endl;
	cout<<"forbidden_sites="<<_data._forbidden_sites.data()<<endl;
	cout<<"crack_switch="<<_data._crack_switch.data()<<endl;
	cout<<"cache_switch="<<_data._cache_switch.data()<<endl;
	cout<<"\n=========================configure file=========================\n";
	
	return 0;
}



