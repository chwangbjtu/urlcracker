#/bin/sh

build()
{
   make clean -C $1
   make -C $1 flags=-O2
}

build ../../../../../Library/funshion/src/kernel/0.1.2/
build ../../../../../Library/funshion/src/thread/0.1.0/src/
build ../../../../../Library/funshion/src/logger/0.2.2/
build ../../../../../Library/funshion/src/netsvc/0.1.4/src/

build util/
build http/
build config/
build redis_mgr/
build ctrl/
build service/
build ./

