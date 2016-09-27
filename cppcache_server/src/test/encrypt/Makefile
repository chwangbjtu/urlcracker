CXX=g++ -g
TARGET=test_encrypt
CPP_LIB := ../../../lib

LIB := $(CPP_LIB)/libencryption.a

HEADER_DIR := ../../encrypt/include

INCLUDE := $(addprefix -I ,$(HEADER_DIR))
$(TARGET):main.cpp
	$(CXX) $(INCLUDE) $^ -o $@ $(LIB) -lcurl -ldl -lssl -lrt

clean:
	rm $(TARGET) -rf
