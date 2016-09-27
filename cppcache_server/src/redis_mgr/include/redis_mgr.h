#ifndef __REDIS_MGR_H
#define __REDIS_MGR_H

//#include "redis_cpp/redisclient.h"    
//#include "redis/redisclient.h"    
#include "redisclient.h"    

#include <boost/shared_ptr.hpp>
#include <boost/date_time.hpp>
#include <boost/format.hpp>

#include <iostream>
#include <string> 
//#include <set>
#include <list>
//#include <map>

//#include <vector>
#include <iterator>
#include <stdlib.h>

#include "../json/json.h"
//#include "json.h"
#include "kmutex.h"
#include "klock.h"

#include "configure.h"

using namespace std;

class redis_mgr
{
public:
        virtual ~redis_mgr() {}
    static redis_mgr* instance();
public:
    int start();
    
    int get_data(std::string&, std::string&);
    int del_data(std::string&);
    int push_list_data(const std::string&);
private:
    redis_mgr(){}
    //bool redis_connect(boost::shared_ptr<redis::client> & client);

    
    bool redis_connect();
    bool is_redis_conn_ok(boost::shared_ptr<redis::client> & client);
    
private:
    static redis_mgr*           _inst;

    std::string _redis_ip;
    int     _redis_port; 
    std::string _redis_pwd; 
    //list<boost::shared_ptr<redis::client> > _client_list;
    boost::shared_ptr<redis::client> _connection;

    //fsk::kshared_mutex _conn_pool_mutex;
    //std::deque< boost::shared_ptr<redis::client> > _conn_pool;
    
    fsk::kshared_mutex          _mutex;

};

#endif//__REDIS_MGR_H


