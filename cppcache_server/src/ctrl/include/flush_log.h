#ifndef __FLUSH_LOG_H
#define __FLUSH_LOG_H
#include "ktask.h"

class flush_log : public fsk::ktask	
{
public:
	flush_log();
	~flush_log();
	virtual int run(const time_t now);
private:
	unsigned int _cnt;
};

#endif //__FLUSH_LOG_H

