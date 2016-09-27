#include <iostream>
#include <signal.h>

#include "tcp_service.h"

#include "dbg.h"
#include "configure.h"
#include "util.h"
#include "tcp_netio.h"
#include "proto_register.h"
#include "security_mgr.h"
#include "tlogger.h"
#include "task_timer.h"
#include "redis_mgr.h"
#include "slave_mgr.h"
#include "json_converter.h"

using namespace std;

int main(int argc,char* argv[])
{
    signal(SIGHUP,SIG_IGN);
    signal(SIGPIPE,SIG_IGN);

    if ( argc == 2 && strncmp(argv[1], "-v", 2) == 0 )
    {
        printf("netserver %s build at %s\r\n", CPPCACHE_SERVER_VERSION, MAKEFILEBUILD_DATE);
        return 0;
    }
    
    util::instance();

    if ( configure::instance()->start("./etc/ct_config.ini") < 0)
    {   
        return -1;
    }
    
    if (security_mgr::instance()->start() < 0) {
        return -1;
    }

    proto_register protoregister;
    protoregister.start();

     //logger 
    if(tlogger::instance()->start() < 0)
    {   
        DBG_ERROR("start logger error");
        return -1;
    }

    if (! redis_mgr::instance()->start())
    {
        DBG_ERROR("redis connect error");
        return -1;
    }

    if (configure::instance()->get_slave_switch() == "on")
    {
        if (! slave_mgr::instance()->start())
        {
            DBG_ERROR("slave connect error");
            return -1;
        }
    }
    task_timer::instance()->start();
    json_converter::instance()->start();

    //start tcp
    netsvc::epoll_accepter<tcp_netio> tcp_acceptor;
    if(tcp_acceptor.start(configure::instance()->get_service_port(),
        configure::instance()->get_service_worker_num()) != 0)
    {
        DBG_ERROR("start tcp accepter failed.");
        return -1;
    }

    while(true)
    {
        sleep(100000);
    }

    return 0;

}
