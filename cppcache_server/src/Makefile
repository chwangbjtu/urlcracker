##target lib###
CXX=g++
TARGET=cppcache_server
FUNSHION_LIB := ../../../../../Library/funshion/lib
FREYJA_LIB := ../../../../../freyja
LOGINSERVER_LIB := ../lib
DEST_ETC := ../bin/etc/
DEST_LOG := ../bin/log/

LIB := $(LOGINSERVER_LIB)/libservice.a
LIB += $(LOGINSERVER_LIB)/libdb_mgr.a
LIB += $(LOGINSERVER_LIB)/libctrl.a
LIB += $(LOGINSERVER_LIB)/libhttp.a
LIB += $(LOGINSERVER_LIB)/libconfig.a
LIB += $(LOGINSERVER_LIB)/libutil.a
LIB += $(LOGINSERVER_LIB)/libjson_linux-gcc-4.1.2_libmt.a
LIB += $(LOGINSERVER_LIB)/libredisclient.a
LIB += $(LOGINSERVER_LIB)/libsecurity.a
LIB += $(LOGINSERVER_LIB)/libencryption.a
LIB += $(FUNSHION_LIB)/kernel/0.1.2/libkernel.a
LIB += $(LOGINSERVER_LIB)/libnetsvc.a
LIB += $(FUNSHION_LIB)/logger/0.2.0/liblogger.a
LIB += $(FUNSHION_LIB)/thread/0.1.0/libthread.a
LIB += $(FUNSHION_LIB)/timer/0.1.0/libtimer.a  
LIB += $(FUNSHION_LIB)/zlib/1.2.4/libz.a
LIB += $(FUNSHION_LIB)/boost/linux_64/libboost_thread.a
LIB += $(FREYJA_LIB)/openssl/openssl-0.9.8zg/lib/libcrypto.a




HEADER_DIR := ../../../../../Library/funshion/include/boost/boost_1_40/
HEADER_DIR += ../../../../../Library/funshion/include/kernel/0.1.2/
HEADER_DIR += ../../../../../Library/funshion/include/logger/0.2.0/
HEADER_DIR += ../../../../../Library/funshion/include/timer/0.1.0 /
HEADER_DIR += ../../../../../Library/funshion/include/thread/0.1.0/
#HEADER_DIR += ../include/json/
HEADER_DIR += ./include/redis/
HEADER_DIR += util/include/
HEADER_DIR += netsvc/include/
HEADER_DIR += security/include/
HEADER_DIR += config/include/
HEADER_DIR += ctrl/include/
HEADER_DIR += redis_mgr/include/
HEADER_DIR += service/include/
HEADER_DIR += ../include/
HEADER_DIR += ./include/


INCLUDE := $(addprefix -I ,$(HEADER_DIR)) 

CXXFLAGS :=${flags} -DMAKEFILEBUILD_DATE="\"`date '+%Y-%m-%d %H:%M:%S'`"\"

SRCS := $(wildcard *.cpp $(SRCDIR)/*.cpp)
OBJS := $(patsubst %.cpp,%.o,$(SRCS))

$(TARGET):$(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@  $(LIB)  -lpthread -lm -lrt -ldl
	cp $(TARGET) ../bin/
	-@if [ ! -d ${DEST_ETC} ]; then mkdir -p ${DEST_ETC}; fi
	-@if [ ! -d ${DEST_LOG} ]; then mkdir -p ${DEST_LOG}; fi
	#cp -f ../etc/* $(DEST_ETC)

$(OBJS):%.o:%.cpp 
	$(CXX) $(INCLUDE) $(CXXFLAGS) -c $< -o $@    

echo:
	echo $(SRCS)
clean:
	-rm -rf $(TARGET) *.o	

check:
	cppcheck -j 4 --enable=all $(INCLUDE) -f -q . 2>cppcheck.log

