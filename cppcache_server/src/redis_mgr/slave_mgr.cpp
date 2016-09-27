#include <stdio.h>
#include <sstream>
#include <vector>
#include "dbg.h"
#include "tlogger.h"
#include "util.h"
#include "slave_mgr.h"
#include "json/json.h"

const string REDIS_NOT_FOUND_KEY = "**nonexistent-key**";

slave_mgr* slave_mgr::_inst = NULL;

slave_mgr* slave_mgr::instance()
{
    if(_inst == NULL)
    {
        _inst = new slave_mgr();
    }
    return _inst;
}

int slave_mgr::start()
{
    _slave_ip = configure::instance()->get_slave_ip();
    _slave_port = configure::instance()->get_slave_port();
    _slave_pwd = configure::instance()->get_slave_pwd();
    _slave_num = configure::instance()->get_slave_num();

    bool res = false;
    res = redis_connect();
    return res;
}

int slave_mgr::get_data(string& key,string& value)
{
    for (int i=0; i<_slave_num; i++)
    {
        bool con = false;
        if ( _slaves[i] && is_redis_conn_ok(_slaves[i]))
        {
            con=true;
        }else{
            con = redis_reconnect(_slaves[i], i);
        }
        if (con)
        {
            int res = get_slave_data(_slaves[i], key, value);
            if (! res)
            {
                return res;
            }
        }
    }
    return -1;//some connection faild or slaves have not data;
}

int slave_mgr::get_slave_data(boost::shared_ptr<redis::client> & client, string& key,string& value)
{
    stringstream ss;
    fsk::kunique_lock<fsk::kshared_mutex> lock(_mutex);
    int res = 0;

    try
    {
        string info = client->get(key);
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


bool slave_mgr::redis_reconnect(boost::shared_ptr<redis::client> & client, int i)
{
    stringstream ss;
    bool res = false;
    try
    {
        //client = boost::shared_ptr<redis::client>((redis::client*)NULL);
        boost::shared_ptr<redis::client> tclient = boost::shared_ptr<redis::client>(new redis::client(_slave_ip, _slave_port+i, _slave_pwd,0));
        if(tclient && is_redis_conn_ok(tclient))
        {
            client = tclient;
            res = true;
        }else{
            tlogger::instance()->log(string("reconnect error"));
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

bool slave_mgr::redis_connect()
{
    stringstream ss;
    bool res = true;
    _slaves.clear();
    for (int i=0; i<_slave_num; i++)
    {
        boost::shared_ptr<redis::client> tclient = boost::shared_ptr<redis::client>((redis::client*)NULL);
        _slaves.push_back(tclient);
    }
    for (int i=0; i<_slave_num; i++)
    {
        try
        {
            boost::shared_ptr<redis::client> tclient = boost::shared_ptr<redis::client>(new redis::client(_slave_ip, _slave_port+i,_slave_pwd,0));
            if(tclient && is_redis_conn_ok(tclient))
            {
                //_slaves.push_back(tclient);
                _slaves[i] = tclient;
            }else{
                tlogger::instance()->log(string("connect error"));
                res =false;
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
    }
    return res;
}

bool slave_mgr::is_redis_conn_ok(boost::shared_ptr<redis::client> & client)
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

