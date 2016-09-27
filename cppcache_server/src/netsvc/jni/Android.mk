LOCAL_PATH := $(call my-dir)/..
include $(CLEAR_VARS)
LOCAL_MODULE:= netsvc

LOCAL_C_INCLUDES += $(LOCAL_PATH)/include

LOCAL_SRC_FILES += \
	linux/epoll_handler.cpp \
	linux/epoll_worker.cpp \
	linux/netsvc_rdwrq.cpp \
	linux/netsvc_util.cpp \
	linux/udp_handler.cpp \
	linux/udp_receiver.cpp \


include $(BUILD_STATIC_LIBRARY)

