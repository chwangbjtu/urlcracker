#ifndef __TLOGGER_H
#define __TLOGGER_H
#include <string>
#include <boost/thread.hpp>

#include "los.h"
#include "logger.h"
#include "writer_file.h"
#include "layout_pattern.h"
#include "writer_buffered.h"
#include "size_cycled_logger.h"
#include "time_cycled_logger.h"

#include "client_req_struct.h"

class tlogger
{
public:
	static tlogger* instance();
	
	int log(std::string info);

    int log(req_struct_t& creq);
	
	int flush();
	
	int start();
	
	//int stop();
	
	//void operator()();
private:
	tlogger();
	static tlogger* _inst;
	//day of this year
	time_t  _last_time;
	fsk::writer *	_wtr;
	fsk::logger* _tlog;
	boost::mutex _mutex;
};
#endif //__TLOGGER_H

