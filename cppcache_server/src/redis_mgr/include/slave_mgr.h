#ifndef __SLAVE_MGR_H
#define __SLAVE_MGR_H

#include "redisclient.h"    

#include <boost/shared_ptr.hpp>
#include <boost/date_time.hpp>
#include <boost/format.hpp>

#include <iostream>
#include <string> 
//#include <set>
#include <list>
//#include <map>

#include <vector>
#include <iterator>
#include <stdlib.h>

#include "../json/json.h"
//#include "json.h"
#include "kmutex.h"
#include "klock.h"

#include "configure.h"

using namespace std;

class slave_mgr
{
public:
        virtual ~slave_mgr() {}
    static slave_mgr* instance();
public:
    int start();
    int get_data(std::string&, std::string&);
private:
    slave_mgr(){}
    int get_slave_data(boost::shared_ptr<redis::client> &, std::string&, std::string&);
    bool redis_connect();
    bool redis_reconnect(boost::shared_ptr<redis::client> & client, int i);
    bool is_redis_conn_ok(boost::shared_ptr<redis::client> & client);
    
private:
    static slave_mgr*           _inst;
    vector < boost::shared_ptr<redis::client> > _slaves;
    fsk::kshared_mutex          _mutex;
    std::string _slave_ip;
    int     _slave_port; 
    std::string _slave_pwd; 
    int     _slave_num; 
};
#endif//__SLAVE_MGR_H


