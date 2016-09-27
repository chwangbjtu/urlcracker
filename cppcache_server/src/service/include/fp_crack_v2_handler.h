#ifndef __FP_CRACK_V2_HANDLER_H
#define __FP_CRACK_V2_HANDLER_H

#include "fp_base_handler.h"
#include <map>
#include <vector>

class fp_crack_v2_handler : public fp_base_handler
{
public:
    fp_crack_v2_handler();
    ~fp_crack_v2_handler();
    virtual int process(const fs::http_request& hr,unsigned int ip,string& vid,string& parsestr,string& resp,unsigned int tid = 0);
    
};

#endif//__FP_CRACK_V1_HANDLER_H

