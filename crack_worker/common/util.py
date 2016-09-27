# -*- coding:utf-8 -*-
import traceback

class ParseType(object):
    DIRECT = "0"
    CUSTOM = "1"

class ErrorCode(object):
    NO_RESPONSE = "0"
    PARAS_ERROR = "1"
    PARSE_ERROR = "2"
    NOT_SUPPORT_SITE = "3"
    NO_EXTRA_INFO = "4"
    UNKNOWN_ERROR = "10"

class Util(object):
   
    @staticmethod
    def parse_site(url):
        try:
            pass
        except Exception as e:
            print traceback.format_exc()
