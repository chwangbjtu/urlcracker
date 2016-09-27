#ifndef __TASK_TIMER_H
#define __TASK_TIMER_H

#include "ktimer.h"

class task_timer
{
public:
	static task_timer* instance();
	~task_timer();
	int start();
private:
	task_timer();
	static task_timer* _inst;
};

#endif//__TASK_TIMER_H


