# -*- coding:utf-8 -*-
import os
import pkgutil
import time
import traceback
from tornado import log
from multiprocessing import Process

import sys
sys.path.append('.')
from monitor.conf import Conf
from monitor.util import Util

'''
cracker检测模块
'''
class CrackerMonitor(Process):

    def __init__(self):
        Process.__init__(self) 

    def check_cracker(self, result, site):
        try:
            if not result or 'error' in result:
                fail_times = self.video_infos[site]['fail'] + 1
                self.video_infos[site]['fail'] = fail_times
                if fail_times > self.send_failed_times:
                    level = 'debug'
                else:
                    level = 'error'
                descript = '破解失败(连续第%s次):错误代码,查阅文档' % fail_times
                if not result:
                    code = ''
                else:
                    code = result['code']
                msg = {'from':'cracker', 'code':code, 'descript':descript, 'site':site, 'level':level} 
                self.util.handle_msg('cracker', msg)
            else:
                #正常后，清零，重新开始
                self.video_infos[site]['fail'] = 0 
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def init_video_infos(self):
        try:
            for item in self.items:
                self.video_infos[item['site']] = {}
                self.video_infos[item['site']]['fail'] = 0
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def load_param(self):
        try:
            #加载cracker
            #1、在此处import方式
            #2、通过映射加载
            #3、切不可在文件开始处import，因为会引发跨进程死锁问题
            self.load_cracker()

            self.util = Util()
            self.send_failed_times = 3
            self.items = [
                {'url':'http://www.letv.com/ptv/vplay/21768679.html', 'site': 'letv', 'vid': 'letv', 'cont_id':'21768679'},
                {'url':'http://m.hunantv.com/#/play/1123577', 'site': 'hunantv', 'vid': 'hunantv', 'cont_id':'1123577'},
                {'url':'http://v.youku.com/v_show/id_XMTI1ODc5MjU2NA==.html', 'site': 'youku', 'vid': 'youku', 'yvid': "XMTI1ODc5MjU2NA=="},
                {'url':'http://tv.sohu.com/20140522/n399900251.shtml', 'site': 'sohu', 'vid': 'sohu', 'svid': '1782552'},
                {'url':"http://www.wasu.cn/wap/Play/show/id/306306", 'site': 'wasu', 'vid': 'wasu', 'wid': '306306'},
                {'url':"http://v.pptv.com/show/NBYCgOhOvvxf3UU.html", 'site': 'pptv', 'vid': 'pptv', 'pptv_id': '23703319'},
                {'url': 'http://www.iqiyi.com/v_19rro2q4mg.html', 'vid': 'iqiyi', 'tvvid': 347655300,'ivid':"be63d714afd883b930f81679d9f05d5f", 'site':'iqiyi'},
                {'url':"http://www.1905.com/vod/play/875911.shtml", 'site': '1905', 'vid': '1905', 'movieid': '2230231', 'duration':10},
                ]
        
            #经过monitor后，video_infos变为:
            #{
            #    "letv":{"fail":"失败次数"},
            #    ...
            #}
            self.video_infos = {}
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def load_cracker(self):
        try:
            self.crackers = {}
            path = os.path.join(os.path.dirname('.'), "cracker")
            modules = pkgutil.iter_modules(path=[path])
            for loader, mod_name, ispkg in modules:
                if mod_name == 'driver':
                    continue
                if mod_name not in sys.modules:
                    loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])
                    class_name = "".join([r.capitalize() for r in mod_name.split('_')])
                    class_name = 'C' + class_name
                    site = mod_name.split('_')[0]
                    loaded_class = getattr(loaded_mod, class_name)
                    self.crackers[site] = loaded_class()
        except Exception, e:
            log.app_log.error(traceback.format_exc())
    
    def run(self):
        times = 0
        self.load_param()
        self.init_video_infos()
        while True:
            try:
                for item in self.items:
                    result = self.crackers[item['site']].crack(item)
                    self.check_cracker(result, item['site'])
            except Exception, e:
                log.app_log.error(traceback.format_exc())
            finally:
                times = times + 1
                descript = 'CrackerMonitor:第%s次检测完毕' % (times,)
                msg = {'from':'cracker', 'code':'', 'descript':descript, 'level':'debug'} 
                self.util.handle_msg('cracker', msg)
                time.sleep(Conf.cracker_monitor_sleep_time)

if __name__ == '__main__':
    test = CrackerMonitor()
    test.start()
