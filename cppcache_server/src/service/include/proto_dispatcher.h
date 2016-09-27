#ifndef __PROTO_DISPATCHER_H
#define __PROTO_DISPATCHER_H
#include <map>
#include <string>
#include "fp_base_handler.h"
using namespace std;

class proto_dispatcher
{
public:
	~proto_dispatcher();
	static proto_dispatcher* instance();

	void reg(string cmd ,fp_base_handler* proto);
	
	//virtual int process(string&req, unsigned int ip,string& vid,string& resp);
	virtual int process(string&req, unsigned int ip,string& vid,string& parsestr,string& resp,unsigned int tid = 0);
    
    virtual int response(string&req, string& resp, unsigned int tid = 0);
private:
	proto_dispatcher();
private:
	static proto_dispatcher* _instance;
	map<string,fp_base_handler*> _dispatcher;//key=(proto_type<< 16 | proto_version)
};

#endif//__PROTO_DISPATCHER_H

