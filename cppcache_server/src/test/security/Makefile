CXX=g++ -g
TARGET=test_crypto
CPP_LIB := ../../../lib
FREYJA_LIB := ../../../../../../../freyja
FUNSHION_LIB := ../../../../../../../Library/funshion

LIB := $(CPP_LIB)/libsecurity.a
LIB += $(CPP_LIB)/libencryption.a
LIB += $(CPP_LIB)/libconfig.a
LIB += $(FUNSHION_LIB)/lib/kernel/0.1.2/libkernel.a
LIB += $(FUNSHION_LIB)/lib/thread/0.1.0/libthread.a
LIB += $(FUNSHION_LIB)/lib/boost/linux_64/libboost_thread.a
LIB += $(FREYJA_LIB)/openssl/openssl-0.9.8zg/lib/libcrypto.a
LIB += $(CPP_LIB)/libjson_linux-gcc-4.1.2_libmt.a

HEADER_DIR := ../../include
HEADER_DIR += $(FUNSHION_LIB)/include/kernel
HEADER_DIR += $(FUNSHION_LIB)/include/curl/curl_7_19_7

INCLUDE := $(addprefix -I ,$(HEADER_DIR))
$(TARGET):main.cpp
	$(CXX) $(INCLUDE) $^ -o $@ $(LIB) -lcurl -ldl -lssl -lrt

clean:
	rm $(TARGET) -rf
