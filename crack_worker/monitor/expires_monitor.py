# -*- coding:utf-8 -*-
import os
import pkgutil
import time
import json
import traceback
from tornado import log
from multiprocessing import Process

import sys
sys.path.append('.')
from monitor.conf import Conf
from monitor.http_client import HttpDownload 
from monitor.util import ParseCrackerType 
from monitor.util import Util 

#Expires检测模块
class ExpiresMonitor(Process):

    def __init__(self):
        Process.__init__(self) 
        #连续出现3次无法获取的累计次数
        self._three_times_count = 0
        #连续出现3次无法获取的累计次数阈值
        #未达到该值事，只在日志中记录
        #达到该值时，发邮件提醒
        self._three_times_alarm = 3

    def check_change_expires_time(self, site, format):
        try:
            now = int(time.time())
            start_time = int(self.video_infos[site][format]['start_time'])
            timestamp = now - start_time
            expires_time = self.video_infos[site][format]['expires_time']
            min_time_field = expires_time - Conf.deviation 
            max_time_field = expires_time + Conf.deviation 
            if timestamp > Conf.expires_monitor_sleep_time:
                #计算出程序检测出的expires_time，当前已超时，故需要减去该轮sleep时间，为比较接近的超时时间
                check_expires_time = timestamp - Conf.expires_monitor_sleep_time
                if expires_time == 0 or check_expires_time < min_time_field or check_expires_time > max_time_field:
                    #第一次运行检测程序，直接将检测出的expires_time赋予item中
                    #或者当前程序检测出的expires_time与上一轮检测出的expires_time进行对比,且超出波动范围
                    self.video_infos[site][format]['expires_time'] = check_expires_time
                    msg = {'from':'expires', 'code':'', 'descript':'程序检测出有效时间出现波动，其值为%s(s)' % check_expires_time, 'site':site, 'format':format, 'level':'debug'}
                    self.util.handle_msg(site, msg)
                    return True 
            return False
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def check_expires(self, url, site, format):
        if not url:
            #获取不到破解的URL地址
            self.video_infos[site][format]['expires'] = True
            self.check_change_expires_time(site, format)
            return 
        #对于网络获取不到数据，测试3遍后才得出结论
        count = 0
        while count < Conf.http_retry_times:
            try:
                #不采用read_body=False，因为有的传过来content-length,但是不能下载
                #result = self.httpclient.get_data(url, ua=self.android_user_agent, read_body=False) 
                if 'hunantv' == site:
                    http_result = self.httpclient.get_data(url, ua=self.android_user_agent) 
                elif 'sohu' == site:
                    http_result = self.httpclient.get_data(url, read_all=True) 
                else:
                    http_result = self.httpclient.get_data(url) 
                if not http_result['data']:
                    msg = {'from':'expires', 'code':http_result['code'], 'descript':http_result['reason'], 'site':site, 'format':format, 'level':'debug'}
                    self.util.handle_msg(site, msg)
                    if count == Conf.http_retry_times - 1:
                        level = 'debug'
                        self._three_times_count += 1
                        if self._three_times_count >= self._three_times_alarm: 
                            level = 'error'
                        else:
                            level = 'debug'
                        msg = {'from':'expires', 'code':'', 'descript':'连接3次无法从破解地址获取数据', 'site':site, 'format':format, 'level':level}
                        self.util.handle_msg(site, msg)
                        self.video_infos[site][format]['expires'] = True
                        self.check_change_expires_time(site, format)
                        return 
                else:
                    #清掉连续3次无法获取的累计数值
                    self._three_times_count = 0
                    data = http_result['data']
                    data = data[-self.hash_content_size:]
                    md5 = self.util.create_md5(data)
                    if self.video_infos[site][format]['md5'] == '':
                        content_length = int(http_result['length'])
                        read_size = int(Conf.http_read_size)
                        if content_length < read_size:
                            content_length_h = self.util.humanization(content_length, 'M') 
                            read_size_h = self.util.humanization(read_size, 'M')
                            msg = {'from':'expires', 'code':'', 'descript':'视频大小%.3f(M)(小于%.3f(M))，请确定是否广告!!!' % (content_length_h, read_size_h), 'site':site, 'format':format, 'level':'error'}
                            self.util.handle_msg(site, msg)
                        self.video_infos[site][format]['md5'] = md5
                        return
                    if self.video_infos[site][format]['md5'] != md5:
                        self.video_infos[site][format]['expires'] = True
                        msg = {'from':'expires', 'code':'', 'descript':'视频破解地址已失效，待统计时间', 'site':site, 'format':format, 'level':'debug'}
                        self.util.handle_msg(site, msg)
                        self.check_change_expires_time(site, format)
                        return 
                    elif self.video_infos[site][format]['md5'] == md5:
                        return
                sleep_time = Conf.http_sleep_time + count * 3; 
                time.sleep(sleep_time)
            except Exception, e:
                log.app_log.error(traceback.format_exc())
            finally:
                count = count + 1


    def init_video_infos(self):
        try:
            for item in self.items:
                self.video_infos[item['site']] = {}
                for format in self.formats:
                    self.video_infos[item['site']][format] = {}
                    self.video_infos[item['site']][format]['expires'] = True
                    self.video_infos[item['site']][format]['expires_time'] = self.expires_times[item['site']]
                    self.video_infos[item['site']][format]['md5'] = ''
                    self.video_infos[item['site']][format]['exists'] = False
                    self.video_infos[item['site']][format]['origin_url'] = ''
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
            self.android_user_agent = 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36' 
            #sohu内容长度应从尾部读取
            self.hash_content_size = 1024 * 1024
            self.formats = ['fluent', 'normal', 'high', 'super', 'original']
            self.expires_times = {
                                'letv':Conf.k_letv_expires_time, 'hunantv':Conf.k_hunantv_expires_time, 'youku':Conf.k_youku_expires_time,
                                'sohu':Conf.k_sohu_expires_time, 'wasu':Conf.k_wasu_expires_time, 'pptv':Conf.k_pptv_expires_time,
                                'iqiyi':Conf.k_iqiyi_expires_time, '1905':Conf.k_1905_expires_time,
                            }
            #支持同一个站点的多个URL
            self.items = [
                        {'url':'http://www.letv.com/ptv/vplay/23270427.html', 'site': 'letv', 'vid': 'letv', 'cont_id':'23270427'},
                        {'url':'http://www.hunantv.com/v/2/157789/f/1802270.html', 'site': 'hunantv', 'vid': 'hunantv', 'cont_id':'1802270'},
                        {'url':'http://v.youku.com/v_show/id_XMTI1ODc5MjU2NA==.html', 'site': 'youku', 'vid': 'youku', 'yvid': "XMTI1ODc5MjU2NA=="},
                        {'url':'http://tv.sohu.com/20140522/n399900251.shtml', 'site': 'sohu', 'vid': 'sohu', 'svid': '1782552'},
                        {'url':'http://www.wasu.cn/Play/show/id/6428315', 'site': 'wasu', 'vid': 'wasu', 'wid': '6428315'},
                        {'url':'http://v.pptv.com/show/lSWtKgwM5iaSHBW0.html', 'site': 'pptv', 'vid': 'pptv', 'pptv_id': '24081045'},
                        {'url': 'http://www.iqiyi.com/v_19rro2q4mg.html', 'vid': 'iqiyi', 'tvvid': 347655300,'ivid':"be63d714afd883b930f81679d9f05d5f", 'site':'iqiyi'},
                        {'url':"http://www.1905.com/vod/play/875911.shtml", 'site': '1905', 'vid': '1905', 'movieid': '2230231', 'duration':10},
                    ]
            self.httpclient = HttpDownload()
            #经过monitor后，video_infos变为:
            #{
            #    "letv":{
            #        "normal":{"url":"破解地址", "start_time":"开始时间戳", "expires":"True", "expires_time":1200, "md5":"部分视频的md5", "exists":"视频是否存在该format", "origin_url":"item中的url"},
            #        "high":{"url":"破解地址", "start_time":"开始时间戳", "expires":"True", "expires_time":1200, "md5":"部分视频的md5", "exists":"视频是否存在该format", "origin_url":"item中的url"},
            #        ...
            #        },
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
                    for format in self.formats:
                        if self.video_infos[item['site']][format]['expires'] == False:
                            pass
                        else:
                            result = self.crackers[item['site']].crack(item)
                            res = self.util.parse_cracker(result, item['site'], format)
                            if res['error'] == ParseCrackerType.CrackerError:
                                #破解程序出现问题，这里不报错，由破解程序的检测程序负责
                                self.video_infos[item['site']][format]['exists'] = False 
                                self.video_infos[item['site']][format]['origin_url'] = '' 
                                self.video_infos[item['site']][format]['expires'] = True
                                continue
                            exists = self.video_infos[item['site']][format]['exists']
                            if not exists and res['error'] == ParseCrackerType.FormatNotFound:
                                #该视频不存在该format，本次又检测到format不存在，则放弃
                                self.video_infos[item['site']][format]['exists'] = False 
                                self.video_infos[item['site']][format]['origin_url'] = '' 
                                self.video_infos[item['site']][format]['expires'] = True
                                continue
                            origin_url = self.video_infos[item['site']][format]['origin_url']
                            if origin_url and origin_url != item['url']:
                                #该format已被其他URL检测占用，无需该URL的该format检测
                                continue
                            url = res['url']
                            self.video_infos[item['site']][format]['url'] = url 
                            self.video_infos[item['site']][format]['start_time'] = time.time()
                            self.video_infos[item['site']][format]['expires'] = False
                            self.video_infos[item['site']][format]['md5'] = ''
                            self.video_infos[item['site']][format]['exists'] = True 
                            self.video_infos[item['site']][format]['origin_url'] = item['url']
                            msg = {'from':'expires', 'code':url, 'descript':'记录当前检测的URL', 'site':item['site'], 'format':format, 'level':'debug'}
                            self.util.handle_msg(item['site'], msg)
                        url = self.video_infos[item['site']][format]['url']
                        self.check_expires(url, item['site'], format)
            except Exception, e:
                log.app_log.error(traceback.format_exc())
            finally:
                times = times + 1
                descript = 'ExpiresMonitor:第%s次检测完毕' % (times,)
                msg = {'from':'expires', 'code':'', 'descript':descript, 'level':'debug'} 
                self.util.handle_msg('expires', msg)
                time.sleep(Conf.expires_monitor_sleep_time)

if __name__ == '__main__':
    test = ExpiresMonitor()
    test.start()
