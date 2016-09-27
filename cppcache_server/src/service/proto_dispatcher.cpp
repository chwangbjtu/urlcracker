#include "dbg.h"
#include "http_request.h"
#include "proto_constant.h"
#include "proto_dispatcher.h"

using  fs::http_request;

proto_dispatcher* proto_dispatcher::_instance = NULL;

proto_dispatcher::proto_dispatcher()
{
}

proto_dispatcher::~proto_dispatcher()
{
}
proto_dispatcher* proto_dispatcher::instance()
{
	if(_instance == NULL)
		_instance = new proto_dispatcher();
	return _instance;
}

void proto_dispatcher::reg(string cmd,fp_base_handler* proto)
{
	_dispatcher.insert(make_pair(cmd,proto));
}

int proto_dispatcher::process(string& req, unsigned int ip,string& vid,string& parsestr,string& resp,unsigned int tid)
{
	http_request hr;
	if ( hr.parse(req.data(),req.size()) < 0) 
	{
		return -1;
	}
	
	string path = hr._req._path;

	map<string,fp_base_handler*>::iterator iter = _dispatcher.find(path);

	if ( iter != _dispatcher.end())
	{
		//return iter->second->process(hr._req._map_params,ip,resp);
		return iter->second->process(hr,ip,vid,parsestr,resp, tid);
	}
	
	return -1;
}

int proto_dispatcher::response(string&req, string& resp, unsigned int tid)
{
    http_request hr;

	if ( hr.parse(req.data(),req.size()) < 0) 
	{
		return -1;
	}

	string path = hr._req._path;
    
    map<string,fp_base_handler*>::iterator iter = _dispatcher.find(path);

	if ( iter != _dispatcher.end())
	{
		return iter->second->response(resp, tid);
	}
	
	return -1;
}

