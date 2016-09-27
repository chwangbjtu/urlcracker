# -*- coding:utf-8 -*-
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

class FlvcdMonitor(Process):

    def __init__(self):
        Process.__init__(self) 
        self.util = Util()
        self.httpclient = HttpDownload()
        self.flvcd_url = 'http://vpwind.flvcd.com/parse-fun.php?url=%s'

    def run(self):
        times = 0
        url = 'http://www.letv.com/ptv/vplay/23270427.html'
        url = self.flvcd_url % url
        while True:
            try:
                text = self.httpclient.get_data(url=url)
                if not text['data']:
                    msg = {'from':'flvcd', 'code':'flvcd_url', 'descript':'无法从硕鼠接口中获取到数据', 'level':'debug'} 
                    self.util.handle_msg('flvcd', msg)
                    continue
                text = text['data'] 
                json_text = json.loads(text)
                second_url = json_text['C']
                msg = {'from':'flvcd', 'code':'second_url', 'descript':second_url, 'level':'debug'} 
                self.util.handle_msg('flvcd', msg)
                text = self.httpclient.get_data(url=second_url)
                if not text['data']:
                    msg = {'from':'flvcd', 'code':'second_url', 'descript':'无法从二次地址中获取到数据', 'level':'debug'} 
                    self.util.handle_msg('flvcd', msg)
                    continue
                text = text['data']
                json_text = json.loads(text)
                real_url = json_text['location']
                msg = {'from':'flvcd', 'code':'real_url', 'descript':real_url, 'level':'debug'} 
                self.util.handle_msg('flvcd', msg)
                video_data = self.httpclient.get_data(real_url) 
                if not video_data['data']:
                    msg = {'from':'flvcd', 'code':'real_url', 'descript':'无法从真实地址中获取到视频数据', 'level':'debug'} 
                    self.util.handle_msg('flvcd', msg)
                    continue
                else:
                    data = video_data['data']
                    content_length = int(video_data['length'])
                    http_read_size = int(Conf.http_read_size)
                    content_length_h = self.util.humanization(content_length, 'M') 
                    http_read_size_h = self.util.humanization(http_read_size, 'M')
                    if content_length < http_read_size:
                        msg = {'from':'flvcd', 'code':'广告', 'descript':'视频大小%.3f(M)(小于%.3f(M))，请确定是否广告!!!' % (content_length_h, http_read_size_h), 'level':'debug'}
                        self.util.handle_msg('flvcd', msg)
                        continue
                    else:
                        msg = {'from':'flvcd', 'code':'正片', 'descript':'视频大小%.3f(M)' % (content_length_h,), 'level':'debug'}
                        self.util.handle_msg('flvcd', msg)
                        continue
            except Exception, e:
                msg = {'from':'flvcd', 'code':'exception', 'descript':traceback.format_exc(), 'level':'debug'} 
                self.util.handle_msg('flvcd', msg)
            finally:
                times = times + 1
                descript = 'FlvcdMonitor:第%s次检测完毕' % (times,)
                msg = {'from':'flvcd', 'code':'', 'descript':descript, 'level':'debug'} 
                self.util.handle_msg('flvcd', msg)
                time.sleep(2 * 60)

if __name__ == '__main__':
    test = FlvcdMonitor()
    test.start()
