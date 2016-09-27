# -*- coding:utf-8 -*-
import os
import re
import time
import random
import json
import urllib
import traceback
import PyV8
from tornado import log
import sys
sys.path.append('.')

from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload
from common.converter import CLetvConverter

class CLetvCracker(object):
        
    cookies = None
    cookie_expires_time = 60 * 60
    le_api = 'http://api.le.com/time?tn=%s'
    user_agent = 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36'

    def __init__(self):

        self.last_update_time = None

        self.isDomain = True
        self.pname = 'MPlayer'
        self._letvc = CLetvConverter()
        self._httpcli = HttpDownload(with_cookie=True)
        self.set_pyv8()


    def set_pyv8(self):
        try:
            ctx = PyV8.JSContext()
            ctx.enter()
            js_data = ''
            js_file = open(os.path.abspath('.') + '/js/letv.js')
            js_data = js_file.read()
            js_file.close()
            self._func = ctx.eval(js_data)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def get_origin_cookie(self, url):
        try:
            #先去请求一遍地址，得到cookie,保存至本地
            cookies = self.create_cookie()
            self._httpcli.get_data(url, ua=self.user_agent, cookies=cookies)
            self.last_update_time = time.time()
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def get_aurl(self, url, os):
        res_url = url
        try:
            if hasattr(self._letvc, 'convert'):
                convert = getattr(self._letvc, 'convert')
                cwurl = convert(url, os, 'web')
                if cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                    if caurl:
                        res_url = caurl
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res_url

    def crack(self, para):
        result = {}
        try:
            origin_url = para['url'] if 'url' in para else ''
            os = para.get('os')
            #if origin_url:
            #    now = time.time()    
            #    if not self.last_update_time or now - self.last_update_time > self.cookie_expires_time:
            #       self.get_origin_cookie(origin_url)
            aurl = self.get_aurl(origin_url, os)
            self.get_origin_cookie(aurl)
            if 'cont_id' in para:
                cont_id = para['cont_id']
                url = self.create_api_url(cont_id)
                if url:
                    resp = self._httpcli.get_data(url, ua=self.user_agent)
                    #print self._httpcli.get_cookie()
                    if resp:
                        seg, format_list = self.real_url_parse(resp, cont_id) 
                        if seg:
                            result['seg'] = seg
                            result['format'] = format_list
                            result['type'] = ParseType.CUSTOM
                            result['start'] = '"location": "'
                            result['end'] = '"'
                        else:
                            result = {'error':1, 'code':ErrorCode.PARSE_ERROR}
                    else:
                        result = {'error':1, 'code':ErrorCode.NO_RESPONSE}
                else:
                    result = {'error':1, 'code':ErrorCode.PARSE_ERROR}
            else:
                result = {'error':1, 'code':ErrorCode.PARAS_ERROR}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error':1, 'code':ErrorCode.UNKNOWN_ERROR}
        finally:
            return result 

    def real_url_parse(self, data, cont_id):
        try:
            regex_express = '\((\{.*\})\)'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(data)
            if not match_result:
                return None, None
            match_result = match_result.groups()[0]
            json_data = json.loads(match_result) 
            if not json_data:
                return None, None
            play_url_data = json_data['playurl'] if 'playurl' in json_data else None
            if not play_url_data:
                return None, None
            #解析出URL的前缀
            url_prefix = None
            domain_data = play_url_data['domain'] if 'domain' in play_url_data else None
            if not domain_data:
                return None, None
            for item in domain_data:
                url_prefix = item
                break
            if not url_prefix:
                return None, None
            #解析出URL的参数
            para = self.create_real_url_para(cont_id)
            para = urllib.urlencode(para)
            #解析出URL的后缀
            dispatch_data = play_url_data['dispatch'] if 'dispatch' in play_url_data else None
            if not dispatch_data:
                return None, None
            name_definition = {"mp4":"fluent", "350":"normal", "1000":"high", "1300":"super"}
            seg = {}
            format_list = []
            for item in dispatch_data:
                if item in name_definition and dispatch_data[item]:
                    url_postfix = dispatch_data[item][0]
                    url = url_prefix + url_postfix + '&' + para
                    seg[name_definition[item]] = [{'url': url, 'duration':''}]
                    format_list.append(name_definition[item])
            return seg, format_list
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None, None

    def create_api_url(self, cont_id):
        try:
            para = self.create_api_url_para(cont_id) 
            if para:
                para = urllib.urlencode(para)
                domain = 'api.le.com' if self.isDomain else 'm.le.com' if self.pname == 'MPlayer' else '117.121.54.104'
                url = 'http://%s/mms/out/video/playJsonH5?%s' % (domain, para)
                return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def create_api_url_para(self, cont_id):
        param = {}
        try:
            tm = self.sync_time_with_letv_server()
            if not tm:
                tm = time.time()
            param = self._func(tm, cont_id)
            if param:
                param = json.loads(param)
                tm = int(tm * 1000)
                rm = int(100 * random.random())
                param['callback'] = 'vjs_%d%d' % (tm, rm)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return param

    def sync_time_with_letv_server(self):
        result = None
        try:
            tn = random.random()
            url = self.le_api % (tn,)
            resp = self._httpcli.get_data(url, ua=self.user_agent) 
            if resp:
                json_data = json.loads(resp)
                result = json_data['stime'] if 'stime' in json_data else None
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result

    def create_real_url_para(self, cont_id):
        para = {}
        try:
            para['format'] = '1'
            para['jsonp'] = ''
            para['expect'] = '3'
            para['p1'] = '0'
            para['p2'] = '04' if 'MPlayer' == self.pname else '06'
            para['termid'] = '2'
            para['ostype'] = 'android'
            para['hwtype'] = 'un'
            para['vid'] = cont_id
            #uuid在每次请求的时候生成(避免出现广告,效仿flvcd的方法)
            para['uuid'] = ''
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return para

    def create_cookie(self):
        result = []
        try:
            tj_lc = self.create_tjlc()
            if not tj_lc:
                #print '失败：加载js代码生成tjlc参数失败'
                log.app_log.error('失败：加载js代码生成tjlc参数失败')
                return result
            result.append({'name':'tj_lc', 'value':tj_lc})
            #print result
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result

    def create_tjlc(self):
        try:
            tj_lc = self._func()
            return tj_lc
        except Exception, e:
            log.app_log.error(traceback.format_exc())


if __name__ == '__main__':
    cracker = CLetvCracker() 
    task = [{'url':'http://www.letv.com/ptv/vplay/21768679.html', 'cont_id':'21768679', 'site':'letv', 'vid':'12345'}]
    for t in task:
        res = cracker.crack(t)
        print json.dumps(res)
