#ifndef __FP_BASE_HANDLER_H
#define __FP_BASE_HANDLER_H
#include <string>
#include <map>

#include "http_request.h"
using namespace std;

typedef map<string, string> KeyValue;

class fp_base_handler
{
public:
	enum
	{
		max_resp_len = 2048
	};

	enum
	{
		return_ok,
		req_invalid
	};
	
	fp_base_handler();
	
	//virtual int process(const multimap<string,string>& req,unsigned int ip,string& resp){return -1;}
	//virtual int process(const fs::http_request& hr,unsigned int ip,string& vid, string& resp){return -1;}

	virtual int process(const fs::http_request& hr,unsigned int ip,string& vid,string& parsestr, string& resp, unsigned int tid = 0){return -1;}
    virtual int response(string& resp, unsigned int tid = 0){return 0;}
	
	virtual ~fp_base_handler(){};
protected:

	int pack(string& msg,string& resp);

	const std::string& find_user_agent(const fs::http_request& hr);
	const unsigned int find_xforwardedfor(const fs::http_request& hr);
    
    int check_param(string& param, string& uid, KeyValue& result, unsigned int tid = 0);
    int parse_param(string& param, KeyValue& result);
    int get_uid(string& param, string& uid); 
    int build_task(KeyValue& result, string& task);

	string _return_succ;
};

#endif //__FP_BASE_HANDLER_H

