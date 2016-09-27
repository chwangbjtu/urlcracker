#include<iostream>
#include<sstream>
#include <arpa/inet.h>
#include <netdb.h>
#include<sstream>	
#include "k_str.h"
#include "dbg.h"
#include "configure.h"
#include "tlogger.h"


using namespace std;
tlogger * tlogger::_inst = NULL;
tlogger * tlogger::instance ()
{
	if (_inst == NULL)
		_inst = new tlogger ();
	return _inst;
}

tlogger::tlogger ()
{
}

int tlogger::log(string info)
{
	boost::mutex::scoped_lock lock(_mutex);
	std::stringstream ss;
	ss<<time(NULL)<<","<<info<<endl;
	string tinfo = ss.str();

	_tlog->log("%s",tinfo.data());
	return 0;
}

int tlogger::log(req_struct_t& creq)
{
    boost::mutex::scoped_lock lock(_mutex);
    std::stringstream ss;
    ss<<time(NULL)<<","<<
        creq._ip<<","<<
        creq._vid<<","<<
        creq._hit<<","<<
        creq._time_out<<","<<
        creq._parse_over<<","<<
        creq._type<<","<<
        creq._body<<endl;
    string tinfo = ss.str();

    _tlog->log("%s",tinfo.data());
    return 0;
}

int tlogger::flush()
{
	boost::mutex::scoped_lock lock(_mutex);
	_tlog->flush();
	return 0;
}

int tlogger::start()
{
	int log_size_mb = 50;
    string log_path = configure::instance()->get_log_path();
	//_wtr = new fsk::writer_buffered(new fsk::writer_file(log_path));
    _tlog = new fsk::time_cycled_logger("cppcache_server_%Y%m%d_%H%M%S.log", fsk::LDAY, new fsk::writer_file(log_path));
	//_tlog = new fsk::size_cycled_logger("cppcache_server_%y%m%d_%H%M%S.log", log_size_mb * 1024 * 1024 , _wtr);
	if (!_tlog)
	{
		cout<<"NULL POINTER _wtr or _log"<<endl;
		return -1;
	}

	_tlog->set_layout(new fsk::layout_pattern("[%t][%T][%l] %m [%L]\r\n"));
	_tlog->open();
	
	//boost::mutex::scoped_lock lock(_mutex);
	/*
        string logpath = configure::instance()->get_log_path();
        _tlog = new fsk::time_cycled_logger("location_server_%H%M%S.log", fsk::LDAY, new fsk::writer_file(logpath));
	_tlog->set_layout(new fsk::layout_pattern("[%t][%T][%l] %m [%L]\r\n"));

	_tlog->open();
	*/
		
	return 0;
}



