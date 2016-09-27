#ifndef JSON_CONVERTER_H
#define JSON_CONVERTER_H
#include <boost/thread.hpp>
#include <string>

using namespace std;

class json_converter
{
public:
    ~json_converter(){}
    static json_converter* instance();

    //thread stuff
    int start();
    int stop();
    void operator()();

public:
    string convertstr(string type,string& jsonstr);

    string json2js(string& jsonstr);

    string json2lua(string& jsonstr);
private:
    int read(std::string);

private:
    json_converter();
    static json_converter* _inst;
    
    string _default_jsstr;
    string _default_luastr;
    char * _convert_arr;
    int _max_convert_len;
    int _nmax_convert_len;

    //thread stuff
    bool _stopped;
    boost::thread* _th;
    time_t _mtime;
    time_t _lasttime;
    off_t _lastsize;
    //r/w lock 
    boost::shared_mutex _mutex;
};

#endif//JSON_CONVERTER_H
