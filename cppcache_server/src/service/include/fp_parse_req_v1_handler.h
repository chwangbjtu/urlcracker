#ifndef __FP_PARSE_REQ_V1_HANDLER_H
#define __FP_PARSE_REQ_V1_HANDLER_H

#include "fp_base_handler.h"

class fp_parse_req_v1_handler: public fp_base_handler
{
public:
	//virtual int process(const fs::http_request& hr,unsigned int ip,string& vid,string& resp);
	virtual int process(const fs::http_request& hr,unsigned int ip,string& vid,string& parsestr,string& resp,unsigned int tid = 0);
private:
	//int unpack(const multimap<string,string>& req,android_req_struct_t& req_struct);
};

#endif//__FP_PARSE_REQ_V1_HANDLER_H

