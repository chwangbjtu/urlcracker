#include "task_timer.h"
#include "flush_log.h" 
#include "configure.h"
#include "dbg.h"

task_timer::task_timer()
{
}

task_timer::~task_timer()
{
}

task_timer* task_timer::_inst = NULL;
task_timer* task_timer::instance()
{
	if(_inst == NULL)
		_inst = new task_timer();
	return _inst;
}

int task_timer::start()
{
	fsk::ktimer<fsk::ktimer_list> * ptimer = new fsk::ktimer<fsk::ktimer_list>;
	ptimer->initialize();
	
	ptimer->schedule(new flush_log(), fsk::ktimeval(1, 0), fsk::ktimeval(1, 0)); 
	
	return 0;
}


