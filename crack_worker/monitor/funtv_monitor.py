# -*- coding:utf-8 -*-
import re
import time
import json
import traceback
from tornado import log
from multiprocessing import Process

import sys
sys.path.append('.')
from monitor.conf import Conf
from monitor.http_client import HttpDownload 
from monitor.util import Util 

class FuntvMonitor(Process):

    def __init__(self):
        Process.__init__(self) 
        self.util = Util()
        self.httpclient = HttpDownload()
        self.funtv_url = 'http://111.161.35.199:7410/crack'
        #self.funtv_url = 'http://suv.fun.tv/ck/v3?uid=lalalala'

    def run(self):
        times = 0
        url = self.funtv_url
        body = '{"vid":"23270427","url":"http://www.letv.com/ptv/vplay/23270427.html","os":"web","site":"letv"}'
        #body = {"k":"556668d1fb6907d3d5d6497ac0fa7f19", "os":"aphone", "site":"sohu", "url":"http://m.tv.sohu.com/20140522/n399900251.shtml", "vid":"4", "extra":""}
        while True:
            try:
                text = self.httpclient.post_data(url=url, body=body)
                if not text['data']:
                    msg = {'from':'funtv', 'code':'funtv_url', 'descript':'无法从破解接口中获取到数据', 'level':'debug'} 
                    self.util.handle_msg('funtv', msg)
                    continue
                text = text['data'] 
                json_text = json.loads(text)
                if 'seg' not in json_text:
                    msg = {'from':'funtv', 'code':'funtv_url', 'descript':'破解失败，无法获取视频数据', 'level':'debug'} 
                    self.util.handle_msg('funtv', msg)
                    continue
                segs = json_text['seg']
                for format in segs.keys():
                    seg = segs[format]
                    url_info = seg[0]
                    second_url = url_info['url']
                    msg = {'from':'funtv', 'code':'second_url', 'descript':second_url, 'level':'debug'} 
                    self.util.handle_msg('funtv', msg)
                    text = self.httpclient.get_data(url=second_url)
                    if not text['data']:
                        msg = {'from':'funtv', 'code':'second_url', 'descript':'无法从二次地址中获取到数据', 'level':'debug'} 
                        self.util.handle_msg('funtv', msg)
                        continue
                    text = text['data']
                    regex_express = '(\{.*\})'      
                    regex_pattern = re.compile(regex_express)
                    match_result = regex_pattern.search(text)
                    if match_result:
                        text = match_result.groups()[0]
                    else:
                        msg = {'from':'funtv', 'code':'second_url', 'descript':'二次地址请求的内容格式有变化', 'level':'debug'} 
                        self.util.handle_msg('funtv', msg)
                        continue
                    json_text = json.loads(text)
                    real_url = json_text['location']
                    msg = {'from':'funtv', 'code':'real_url', 'descript':real_url, 'level':'debug'} 
                    self.util.handle_msg('funtv', msg)
                    video_data = self.httpclient.get_data(real_url) 
                    if not video_data['data']:
                        msg = {'from':'funtv', 'code':'real_url', 'descript':'无法从真实地址中获取到视频数据', 'level':'debug'} 
                        self.util.handle_msg('funtv', msg)
                        continue
                    else:
                        data = video_data['data']
                        content_length = int(video_data['length'])
                        http_read_size = int(Conf.http_read_size)
                        content_length_h = self.util.humanization(content_length, 'M') 
                        http_read_size_h = self.util.humanization(http_read_size, 'M')
                        if content_length < http_read_size:
                            msg = {'from':'funtv', 'code':'广告', 'descript':'视频大小%.3f(M)(小于%.3f(M))，请确定是否广告!!!' % (content_length_h, http_read_size_h), 'level':'debug'}
                            self.util.handle_msg('funtv', msg)
                        else:
                            msg = {'from':'funtv', 'code':'正片', 'descript':'视频大小%.3f(M)' % (content_length_h,), 'level':'debug'}
                            self.util.handle_msg('funtv', msg)
                        break
            except Exception, e:
                msg = {'from':'funtv', 'code':'exception', 'descript':traceback.format_exc(), 'level':'debug'} 
                self.util.handle_msg('funtv', msg)
            finally:
                times = times + 1
                descript = 'FuntvMonitor:第%s次检测完毕' % (times,)
                msg = {'from':'funtv', 'code':'', 'descript':descript, 'level':'debug'} 
                self.util.handle_msg('funtv', msg)
                time.sleep(2 * 60)

if __name__ == '__main__':
    test = FuntvMonitor()
    test.start()
