#/bin/sh

build()
{
   make clean -C $1
   make -C $1 flags=-O2
}

build netsvc/
build encrypt/
build security/
build util/
build http/
build config/
build redis_mgr/
build ctrl/
build service/
build ./

