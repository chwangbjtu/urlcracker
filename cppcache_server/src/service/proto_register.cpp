#include "proto_register.h"

#include "fp_parse_req_v1_handler.h"
#include "fp_crack_v2_handler.h"
#include "fp_crack_v3_handler.h"
#include "proto_dispatcher.h"
#include "proto_constant.h"
#include "configure.h"
bool proto_register::init = false;

int proto_register::start()
{
	if ( !init)
	{
		init = true;

        //proto_dispatcher::instance()->reg("/parse",new fp_parse_req_v1_handler());
        string crack_switch  = configure::instance()->get_crack_switch();
		if ( crack_switch == "on")
		{
			proto_dispatcher::instance()->reg("/crack",new fp_parse_req_v1_handler());
		}
        //proto_dispatcher::instance()->reg("/ck/v2",new fp_crack_v2_handler());
        proto_dispatcher::instance()->reg("/ck/v3",new fp_crack_v3_handler());
		
	}
	return 0;
}

