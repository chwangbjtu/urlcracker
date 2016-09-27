# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import os
#import PyV8
import re

import sys
sys.path.append('.')
import commands
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload
from common.converter import CIqiyiConverter

class IqiyiH5Driver(object):
    cookie_expires_time = 60 * 60
    user_agent = 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36' 
    def __init__(self):
        #self._ctx = PyV8.JSContext()
        #self._ctx.enter()
        #load js
        self._js = ""
        base_dir = os.path.abspath(".")
        filename = base_dir + "/js/iqiyi.js"
        #filename = base_dir + "/js/test.js"
        self._phantomjs_cmd = "/home/wangchao/phantomjs-2.1.1-linux-x86_64/bin/phantomjs ./phantomjs/iqiyi.js %s %s"
        jsfile = open(filename)
        try:
            self._js = jsfile.read( )
        finally:
            jsfile.close()

        #self._func = self._ctx.eval(self._js)
        self._iqiyivc = CIqiyiConverter()
        self._httpcli = HttpDownload()
    def get_aurl(self, url, os):
        res_url = url
        try:
            if hasattr(self._iqiyivc, 'convert'): 
                convert = getattr(self._iqiyivc, 'convert')
                cwurl = convert(url, os, 'web')
                if  cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                    if caurl:
                        res_url = caurl    
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res_url
    def parse_body(self,data):
        result = {}
        try:
            regex_express = 'Q\.PageInfo\.playInfo\.tvid[ ]?=[ ]?\"(\d+)\"[ ]?'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(data)
            if match_result:
                match_result = match_result.groups()[0]
                result['tvid'] = match_result
            regex_express = 'Q\.PageInfo\.playInfo\.vid[ ]?=[ ]?\"(\d|\w+)\"[ ]?'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(data)
            if match_result:
                match_result = match_result.groups()[0]
                result['vid'] = match_result
            return result
        except Exception,e:
           log.app_log.error(traceback.format_exc())

    def real_url_parse(self,data):
        try:
            name_definition = ["fluent","high"]
            #resurl = self._func(data["tvvid"],data["ivid"])
            cmd = self._phantomjs_cmd % (data["tvvid"],data["ivid"])
            print cmd
            resurl = commands.getoutput(cmd)
            print resurl
            seg = {}
            seg["fluent"]=[{'url': resurl, 'duration':''}]
            url = resurl.replace("rate=1","rate=2")
            seg["high"]=[{'url': url, 'duration':''}]
            return seg,name_definition
        except Exception,e:
            log.app_log.error(traceback.format_exc())

    def parse(self, para):
        #log.app_log.info('%s : %s' % (self.__class__.__name__, json.dumps(para)))
        result = {}
        try:
            origin_url = para['url'] if 'url' in para else ''
            tvvid = para['tvvid'] if 'tvvid' in para else ''
            ivid = para['ivid'] if 'ivid' in para else ''
            
            seg, format_list = self.real_url_parse(para)
            if seg:
                result['seg'] = seg
                result['format'] = format_list
                result['type'] = ParseType.CUSTOM
                result['start'] = '"m3u":"'
                result['end'] = '"'
            else:
                result = {'error':1, 'code':ErrorCode.PARSE_ERROR}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    iqiyi = CIqiyiCracker()
    para = {'url': 'http://www.iqiyi.com/v_19rro2q4mg.html', 'vid': 2233, 'tvvid': 347655300,'ivid':"be63d714afd883b930f81679d9f05d5f", 'site':'iqiyi'}
    res = iqiyi.parse(para)
    print json.dumps(res)
