//#include "const_struct.h"
//#include "cmd_constant.h"
#include <stdio.h>
#include <sstream>
#include <vector>
#include "dbg.h"
#include "tlogger.h"
#include "util.h"
#include "redis_mgr.h"
#include "json/json.h"

const string REDIS_NOT_FOUND_KEY = "**nonexistent-key**";

redis_mgr* redis_mgr::_inst = NULL;

redis_mgr* redis_mgr::instance()
{
    if(_inst == NULL)
    {
        _inst = new redis_mgr();
    }
    return _inst;
}

int redis_mgr::start()
{
    _redis_ip     = configure::instance()->get_redis_ip();
    _redis_port   = configure::instance()->get_redis_port();
    _redis_pwd   = configure::instance()->get_redis_pwd();

    bool res = false;
    //res = redis_connect( _connection);
    res = redis_connect();

    return res;
}

int redis_mgr::del_data(string& key)
{
    stringstream ss;
    fsk::kunique_lock<fsk::kshared_mutex> lock(_mutex);
    int res = 0;
    if ( is_redis_conn_ok( _connection))
    {;}
    else
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"not conn ok,need reconnect";
        tlogger::instance()->log(ss.str());
        ss.str("");
        redis_connect();
    }
    if ( res != 0)   
        return res;
	
	try
	{
        if ( ! _connection)
        {
            ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"not connected,after reconnection";
            tlogger::instance()->log(ss.str());
            ss.str("");
            return -1;
        }
        res = _connection->del(key);
	}
    catch(redis::connection_error &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }
    catch(exception &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }
    catch(...)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"get json data throw err";
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
        //continue; 
    }
	return res;
}
int redis_mgr::get_data(string& key,string& value)
{
    stringstream ss;
    fsk::kunique_lock<fsk::kshared_mutex> lock(_mutex);
    int res = 0;
    if ( is_redis_conn_ok( _connection))
    {;}
    else
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"not conn ok,need reconnect";
        tlogger::instance()->log(ss.str());
        ss.str("");
        redis_connect();
    }

    if ( res != 0)   
        return res;
 
    try
    {
        if ( ! _connection)
        {
            ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"not connected,after reconnection";
            tlogger::instance()->log(ss.str());
            ss.str("");
            return -1;
        }
        string info = _connection->get(key);
        if ( info == REDIS_NOT_FOUND_KEY)
        {
            //tlogger::instance()->log(string("can not find key,") + key);
            return -1;
        }
		
        //针对letv将动态生成uuid
        vector<string> split_keys;
        util::instance()->split(key, ":", split_keys);
        if (split_keys.size() != 3)
        {
            value = info;
        }else{
            string site = split_keys[1];
            if (site == "letv")
            {
                //生成uuid
                int64_t curr_time = util::instance()->get_current_time();
                char uuid[64];
                sprintf(uuid, "&uuid=%ld", curr_time);

                Json::Reader reader;
                Json::Value json_value;
                if (!reader.parse(info, json_value) || json_value.type() != Json::objectValue) 
                {
                    value = info;
                    return res;
                }
                Json::Value segs = json_value["seg"];
                Json::Value::Members formats = segs.getMemberNames();
                int formats_size = formats.size();
                for (int i=0; i < formats_size; i++)
                {
                    string format = formats[i];
                    Json::Value urls = segs[format];
                    int urls_size = urls.size();
                    for (int j=0; j < urls_size; j++)
                    {
                        Json::Value url = urls[j];
                        string video_url = url["url"].asString();
                        video_url = video_url + uuid;
                        url["url"] = video_url;
                        urls[j] = url;
                    }
		            segs[format] = urls;
                }
		        json_value["seg"] = segs;
                Json::FastWriter writer;
                value = writer.write(json_value);
            }else{
                value = info;
            }
        }
    }
    catch(redis::connection_error &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }
    catch(exception &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }
    catch(...)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"get json data throw err";
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
        //continue; 
    }

    return res;
}

int redis_mgr::push_list_data(const string& data)
{
    stringstream ss;
    fsk::kunique_lock<fsk::kshared_mutex> lock(_mutex);
    int res = 0;
    if ( is_redis_conn_ok( _connection))
    {;}
    else
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"not conn ok,need reconnect";
        tlogger::instance()->log(ss.str());
        ss.str("");
        redis_connect();
    }   

    try
    {
        if ( ! _connection)
        {
            ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"not connected,after reconnection";
            tlogger::instance()->log(ss.str());
            ss.str("");
            res = -1;;
        }
        else
        {
            //string info = _connection->get(key);
            //redis::command cmd = redis::makecmd("LPUSH") <<redis::key("crack_task_list")<<data;
            redis::command cmd = redis::makecmd("LPUSH") <<redis::key("crack:task:queue")<<data;
            std::vector<redis::command> vec;
            vec.push_back(cmd);
            _connection->exec_transaction(vec);
        }
    }
    catch(redis::connection_error &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }
    catch(exception &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }
    catch(...)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"lpush data throw err";
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = -1;
    }

    return res;
}

//bool redis_mgr::redis_connect(boost::shared_ptr<redis::client> & client)
bool redis_mgr::redis_connect()
{
    stringstream ss;
    bool res = false;
    try
    {
        _connection = boost::shared_ptr<redis::client>((redis::client*)NULL);
        //string pass = "123456";
        boost::shared_ptr<redis::client> tclient = boost::shared_ptr<redis::client>(new redis::client(_redis_ip, _redis_port,_redis_pwd,0));
        //boost::shared_ptr<redis::client> tclient = boost::shared_ptr<redis::client>(new redis::client("redis://tt:123456@192.168.16.155:6379"));
        if(tclient)
        {
            //fsk::kunique_lock<fsk::kshared_mutex> lock(_conn_pool_mutex);
            //_conn_pool.push_back(client);
            /*
            redisReply* r = (redisReply*)redisCommand(tclient, "AUTH %s", "123456");
            if (reply->type == REDIS_REPLY_ERROR) 
            { 
                DBG_ERROR("connect error ,pwd error");
            }
            */
            //tclient->auth("123456");
            
            _connection = tclient;
            //_connection->auth("123456");
            //client = tclient;
            res = true;
        }
        else
        {
            tlogger::instance()->log(string("reconnect error"));
            _connection = boost::shared_ptr<redis::client>((redis::client*)NULL);
        }
    }
    catch(redis::connection_error &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
    }
    catch(exception &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
    }
    catch(...)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"connect redis error";
        tlogger::instance()->log(ss.str());
        ss.str("");
    }

    return res;
}

bool redis_mgr::is_redis_conn_ok(boost::shared_ptr<redis::client> & client)
{
    stringstream ss;
    bool res = false;
    try
    {
        if(client)
        {
            res =  !client->exists("Do-You-Believe-God?");
        }
    }
    catch(redis::connection_error &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res =  false;
        boost::shared_ptr<redis::client>((redis::client*)NULL);
    }
    catch(exception &err)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<err.what();
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = false;    
    }
    catch(...)
    {
        ss<<__FUNCTION__<<":"<<__LINE__<<":"<<"connect redis error";
        tlogger::instance()->log(ss.str());
        ss.str("");
        res = false;
    }
    
    return res;
}



