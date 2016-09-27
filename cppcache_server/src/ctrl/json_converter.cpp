#include <sys/types.h>
#include <sys/stat.h>
#include<iostream>
//#include <algorithm>
#include <cstddef>
#include <fstream>
#include <boost/algorithm/string/replace.hpp>
#include "dbg.h"
#include "json_converter.h"

json_converter* json_converter::_inst = NULL;
json_converter* json_converter::instance()
{
        if ( _inst == NULL)
                _inst = new json_converter();
        return _inst;
}

json_converter::json_converter()
{
    _max_convert_len = 1024*1024*4;
    _nmax_convert_len = 1024*1024*36;
    _convert_arr = new char [_max_convert_len*2];
}

string json_converter::convertstr(string parsestr,string& jsonstr)
{
    string data;
    if ( parsestr == "js")
    {
        data = json_converter::instance()->json2js(jsonstr);
    }
    else if ( parsestr == "lua")
    {
        data = json_converter::instance()->json2lua(jsonstr);
    }
    else
    {
        data = jsonstr;
    }

    return data;
}

string json_converter::json2js(string& jsonstr)
{
    boost::shared_lock<boost::shared_mutex> lock(_mutex);
    string sres;
    if (jsonstr.size() + _default_jsstr.size() > _max_convert_len)
    {
        delete _convert_arr;
        _max_convert_len = _max_convert_len * 2;

        if ( _max_convert_len > _nmax_convert_len)
        {
            return sres;
        }
        _convert_arr = new char [_max_convert_len*2];
    }
    string send;
   
    if ( jsonstr.find('\\') != string::npos) 
    {
        string t = "\\\\";
        boost::replace_all(jsonstr, "\\", "\\\\");
        //std::replace( jsonstr.begin(), jsonstr.end(), '\\', t.data());
        /*
        int i = 0;
        for (i = 0;i<jsonstr.size();i++)
        {
            if (jsonstr[i]=='\\')
            {
                send.append("\\",1);
                send.append("\\",1);
            }
            else
            {
                send.append(&jsonstr[i],1);
            }
        }
        */
    }
    else
    {
        //send = jsonstr;
        ;
    }

    int len = snprintf(_convert_arr,_max_convert_len,_default_jsstr.data(),jsonstr.data());
    //int len = snprintf(_convert_arr,_max_convert_len,_default_jsstr.data(),send.data());
    sres.assign(_convert_arr,len);

    return sres;
}

string json_converter::json2lua(string& jsonstr)
{
    boost::shared_lock<boost::shared_mutex> lock(_mutex);

    string sres;
    return sres;
}

int json_converter::read(string file)
{
    //check is it necessary to read file
    struct stat st;
    if ( lstat(file.c_str(), &st) == 0)
    {
        if ( st.st_mtime == _lasttime && st.st_size == _lastsize)
        {
            return 0;
        }
    }
    else
    {
        DBG_ERROR("lstat file error");
        return -1;
    }

    ifstream fin(file.data());
    string str;
    string fstr;

    while(getline(fin, str))
    {
        fstr.append(str);
    }

    boost::unique_lock<boost::shared_mutex> lock(_mutex);//write lock

    _default_jsstr = fstr;

    return 0;
}

int json_converter::start()
{
    try 
    {
        _stopped = false;
        _th = new boost::thread(boost::ref(*this));
    } 
    catch(const std::exception& e) 
    {
        DBG_ERROR("create json_converter reading thread failed.");
        _stopped = true;
        return -1;
    }
    return 0;
}
int json_converter::stop()
{
    if ( _stopped)
    {
        return 0;
    }
    _stopped = true;
    _th->join();
    delete _th;
    return 0;
}

void json_converter::operator()()
{
    while ( !_stopped) 
    {
        if ( read("etc/json2js.template") < 0 ) 
        {
            fprintf(stderr,"failed to read the json_converter.bin  error.\n");
        }
        boost::xtime tm;
        boost::xtime_get(&tm,boost::TIME_UTC);
        tm.sec += 10;
        boost::thread::sleep(tm);

    }
}
