#ifndef __DBG_H
#define __DBG_H

#include <time.h>
#include <stdio.h>

#define DBG_INFO(format, args...) do {                                        		 	\
         do{                                                                                             	\
                   time_t lt = time(NULL);                                                 		\
                   struct tm *ptr = localtime(&lt);                                     			\
                   char str[64] = {0};                                                              	\
                   strftime(str,63,"[%Y%m%d%H%M%S][info]: ", ptr);				\
                   printf(str);                                                                               \
                   printf(format,##args);                                       				\
         }while(0);                                                                          			\
         printf("[ file: %s, line: %d ]", __FILE__, __LINE__);                       		\
         putchar('\n');                                                                             		\
         fflush(stdout);                                                                          		\
} while(0)


#define DBG_WARNING(format, args...) do {                                         	\
         do{                                                                                             	\
                   time_t lt = time(NULL);                                                 		\
                   struct tm *ptr = localtime(&lt);                                     			\
                   char str[64] = {0};                                                              	\
                   strftime(str,63,"[%Y%m%d%H%M%S][warning]: ", ptr);			\
                   printf(str);                                                                               \
                   printf(format,##args);                                       				\
         }while(0);                                                                          			\
         printf("[ file: %s, line: %d ]", __FILE__, __LINE__);                       		\
         putchar('\n');                                                                             		\
         fflush(stdout);                                                                          		\
} while(0)

#define DBG_ERROR(format, args...) do {                                         		\
         do{                                                                                             	\
                   time_t lt = time(NULL);                                                 		\
                   struct tm *ptr = localtime(&lt);                                     			\
                   char str[64] = {0};                                                              	\
                   strftime(str,63,"[%Y%m%d%H%M%S][error]: ", ptr);				\
                   printf(str);                                                                               \
                   printf(format,##args);                                       				\
         }while(0);                                                                          			\
         printf("[ file: %s, line: %d ]", __FILE__, __LINE__);                       		\
         putchar('\n');                                                                             		\
         fflush(stdout);                                                                          		\
} while(0)

#define DBG_FATAL(format, args...) do {                                         		\
         do{                                                                                             	\
                   time_t lt = time(NULL);                                               	  		\
                   struct tm *ptr = localtime(&lt);                                     			\
                   char str[64] = {0};                                                              	\
                   strftime(str,63,"[%Y%m%d%H%M%S][fatal]: ", ptr);				\
                   printf(str);                                                                               \
                   printf(format,##args);                                       				\
         }while(0);                                                                          			\
         printf("[ file: %s, line: %d ]", __FILE__, __LINE__);                       		\
         putchar('\n');                                                                             		\
         fflush(stdout);                                                                          		\
} while(0)

#define _TEST 0														

#ifndef _TEST
#define DBG_TEST(format, args...) do {                                         			\
         do{                                                                                             	\
                   time_t lt = time(NULL);                                                 		\
                   struct tm *ptr = localtime(&lt);                                     			\
                   char str[64] = {0};                                                              	\
                   strftime(str,63,"[%Y%m%d%H%M%S][test]: ", ptr);				\
                   printf(str);                                                                               \
                   printf(format,##args);                                       				\
         }while(0);                                                                          			\
         printf("[ file: %s, line: %d ]", __FILE__, __LINE__);                       		\
         putchar('\n');                                                                             		\
         fflush(stdout);                                                                          		\
} while(0)
#else
#define DBG_TEST(...)do{\
}while(0);
#endif

#endif //__DBG_H


