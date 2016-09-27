# -*- coding:utf-8 -*-
from tornado import log
import datetime
import time
import traceback
import json
import sys
import re
sys.path.append(".")

class BaseConverter(object):
    def __init__(self):
        pass

    def convert(self, url, from_os, to_os):
        try:
            if not url:
                return url
            if from_os == to_os:
                return url
            method = 'conv_%s_to_%s' % (from_os, to_os)
            if hasattr(self, method):
                conv_fun = getattr(self, method)
                return conv_fun(url)
            else:
                return None
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CYoukuConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            return url + "?x"
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            return url[:-2]
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            return url + "?x"
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            return url[:-2]
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            return url + "?x"
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            return url[:-2]
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            return url + "?x"
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x
            #http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html
            return url[:-2]
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CTudouConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CQqConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_web(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html

            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html

            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html

            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html

            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html
            #http://m.v.qq.com/cover/0/01ga9d6hkd9r4d9.html 

            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html
            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63

            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html
            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            if 'v.qq.com' in url:
                regex_express = 'v\.qq\.com\/(.*)\.html'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    paths = match_result.split('/')
                    if len(paths) == 4:
                        return 'http://m.v.qq.com/%s/%s/%s.html?vid=%s' % (paths[0], paths[1], paths[2], paths[3])
                    else:
                        return url.replace('v.qq.com', 'm.v.qq.com')
            elif 'film.qq.com' in url: 
                return url.replace('/cover/', '/weixin/detail/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.v.qq.com/cover/0/01ga9d6hkd9r4d9.html 
            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html

            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63
            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html

            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html
            if 'm.v.qq.com' in url:
                regex_express = 'm\.v\.qq\.com(.*)\.html\?vid=(\w+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result and len(match_result.groups()) == 2:
                    return 'http://v.qq.com%s/%s.html' % (match_result.groups()[0], match_result.groups()[1])
                else:
                    return url.replace('m.v.qq.com', 'v.qq.com')
            elif 'film.qq.com' in url: 
                return url.replace('/weixin/detail/', '/cover/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html
            #http://m.v.qq.com/cover/0/01ga9d6hkd9r4d9.html 

            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html
            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63

            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html
            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            if 'v.qq.com' in url:
                regex_express = 'v\.qq\.com\/(.*)\.html'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    paths = match_result.split('/')
                    if len(paths) == 4:
                        return 'http://m.v.qq.com/%s/%s/%s.html?vid=%s' % (paths[0], paths[1], paths[2], paths[3])
                    else:
                        return url.replace('v.qq.com', 'm.v.qq.com')
            elif 'film.qq.com' in url: 
                return url.replace('/cover/', '/weixin/detail/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.v.qq.com/cover/0/01ga9d6hkd9r4d9.html 
            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html

            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63
            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html

            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html
            if 'm.v.qq.com' in url:
                regex_express = 'm\.v\.qq\.com(.*)\.html\?vid=(\w+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result and len(match_result.groups()) == 2:
                    return 'http://v.qq.com%s/%s.html' % (match_result.groups()[0], match_result.groups()[1])
                else:
                    return url.replace('m.v.qq.com', 'v.qq.com')
            elif 'film.qq.com' in url: 
                return url.replace('/weixin/detail/', '/cover/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html
            #http://m.v.qq.com/cover/0/01ga9d6hkd9r4d9.html 

            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html
            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63

            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html
            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            if 'v.qq.com' in url:
                regex_express = 'v\.qq\.com\/(.*)\.html'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    paths = match_result.split('/')
                    if len(paths) == 4:
                        return 'http://m.v.qq.com/%s/%s/%s.html?vid=%s' % (paths[0], paths[1], paths[2], paths[3])
                    else:
                        return url.replace('v.qq.com', 'm.v.qq.com')
            elif 'film.qq.com' in url: 
                return url.replace('/cover/', '/weixin/detail/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.v.qq.com/cover/0/01ga9d6hkd9r4d9.html 
            #http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html

            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63
            #http://v.qq.com/cover/j/jwzfwv97k7xukzd/z0016fa0l63.html

            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            #http://film.qq.com/cover/2/2nh6bsl6mlxm7bf.html
            if 'm.v.qq.com' in url:
                regex_express = 'm\.v\.qq\.com(.*)\.html\?vid=(\w+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result and len(match_result.groups()) == 2:
                    return 'http://v.qq.com%s/%s.html' % (match_result.groups()[0], match_result.groups()[1])
                else:
                    return url.replace('m.v.qq.com', 'v.qq.com')
            elif 'film.qq.com' in url: 
                return url.replace('/weixin/detail/', '/cover/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CSohuConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://tv.sohu.com/20150513/n412986358.shtml
            #http://pad.tv.sohu.com/20150513/n412986358.shtml
            return url.replace('tv.sohu.com', 'pad.tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://pad.tv.sohu.com/20150513/n412986358.shtml
            #http://tv.sohu.com/20150513/n412986358.shtml
            return url.replace('pad.tv.sohu.com', 'tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://tv.sohu.com/20150513/n412986358.shtml
            #http://m.tv.sohu.com/20150513/n412986358.shtml
            return url.replace('tv.sohu.com', 'm.tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.tv.sohu.com/20150513/n412986358.shtml
            #http://tv.sohu.com/20150513/n412986358.shtml
            return url.replace('m.tv.sohu.com', 'tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://tv.sohu.com/20150513/n412986358.shtml
            #http://m.tv.sohu.com/20150513/n412986358.shtml
            return url.replace('tv.sohu.com', 'm.tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.tv.sohu.com/20150513/n412986358.shtml
            #http://tv.sohu.com/20150513/n412986358.shtml
            return url.replace('m.tv.sohu.com', 'tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://tv.sohu.com/20150513/n412986358.shtml
            #http://m.tv.sohu.com/20150513/n412986358.shtml
            return url.replace('tv.sohu.com', 'm.tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.tv.sohu.com/20150513/n412986358.shtml
            #http://tv.sohu.com/20150513/n412986358.shtml
            return url.replace('m.tv.sohu.com', 'tv.sohu.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CIqiyiConverter(BaseConverter):
    def __init__(self):
        pass
    def conv_web_to_web(self,url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())
    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.iqiyi.com/v_19rrnnrs34.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.iqiyi.com/v_19rrnnrs34.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.iqiyi.com/v_19rrnnrs34.html
            #http://m.iqiyi.com/v_19rrnnrs34.html
            return url.replace('www.iqiyi.com', 'm.iqiyi.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.iqiyi.com/v_19rrnnrs34.html
            #http://www.iqiyi.com/v_19rrnnrs34.html
            return url.replace('m.iqiyi.com', 'www.iqiyi.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.iqiyi.com/v_19rrnnrs34.html
            #http://m.iqiyi.com/v_19rrnnrs34.html
            return url.replace('www.iqiyi.com', 'm.iqiyi.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.iqiyi.com/v_19rrnnrs34.html
            #http://www.iqiyi.com/v_19rrnnrs34.html
            return url.replace('m.iqiyi.com', 'www.iqiyi.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.iqiyi.com/v_19rrnnrs34.html
            #http://m.iqiyi.com/v_19rrnnrs34.html
            return url.replace('www.iqiyi.com', 'm.iqiyi.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.iqiyi.com/v_19rrnnrs34.html
            #http://www.iqiyi.com/v_19rrnnrs34.html
            return url.replace('m.iqiyi.com', 'www.iqiyi.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CLetvConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.letv.com/ptv/vplay/21768679.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.letv.com/ptv/vplay/21768679.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.letv.com/ptv/vplay/21768679.html
            #http://m.letv.com/vplay_21768679.html
            url = url.replace('letv.com', 'le.com')
            return url.replace('www.le.com/ptv/vplay/', 'm.le.com/vplay_')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.letv.com/vplay_21768679.html
            #http://www.letv.com/ptv/vplay/21768679.html
            url = url.replace('letv.com', 'le.com')
            return url.replace('m.le.com/vplay_', 'www.le.com/ptv/vplay/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.letv.com/ptv/vplay/21768679.html
            #http://m.letv.com/vplay_21768679.html
            url = url.replace('letv.com', 'le.com')
            return url.replace('www.le.com/ptv/vplay/', 'm.le.com/vplay_')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.letv.com/vplay_21768679.html
            #http://www.letv.com/ptv/vplay/21768679.html
            url = url.replace('letv.com', 'le.com')
            return url.replace('m.le.com/vplay_', 'www.le.com/ptv/vplay/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.letv.com/ptv/vplay/21768679.html
            #http://m.letv.com/vplay_21768679.html
            url = url.replace('letv.com', 'le.com')
            return url.replace('www.le.com/ptv/vplay/', 'm.le.com/vplay_')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.letv.com/vplay_21768679.html
            #http://www.letv.com/ptv/vplay/21768679.html
            url = url.replace('letv.com', 'le.com')
            return url.replace('m.le.com/vplay_', 'www.le.com/ptv/vplay/')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class C1905Converter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.1905.com/vod/play/623659.shtml
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CKankanConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027
            #http://m.kankan.com/v/70/70763.shtml?subid=303027

            #http://vip.kankan.com/vod/84870.html
            if 'vod.kankan.com' in url:
                return url.replace('vod.kankan.com', 'm.kankan.com')
            elif 'vip.kankan.com' in url:
                return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.kankan.com/v/70/70763.shtml?subid=303027
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027

            #http://vip.kankan.com/vod/84870.html
            if 'm.kankan.com' in url:
                return url.replace('m.kankan.com', 'vod.kankan.com')
            elif 'vip.kankan.com' in url:
                return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027
            #http://m.kankan.com/v/70/70763.shtml?subid=303027

            #http://vip.kankan.com/vod/84870.html
            #http://m.vip.kankan.com/play.html?movieid=84870
            if 'vod.kankan.com' in url:
                return url.replace('vod.kankan.com', 'm.kankan.com')
            elif 'vip.kankan.com' in url:
                regex_express = '(\d+)\.html'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    return 'http://m.vip.kankan.com/play.html?movieid=%s' % match_result
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.kankan.com/v/70/70763.shtml?subid=303027
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027

            #http://m.vip.kankan.com/play.html?movieid=84870
            #http://vip.kankan.com/vod/84870.html
            if 'm.kankan.com' in url:
                return url.replace('m.kankan.com', 'vod.kankan.com')
            elif 'm.vip.kankan.com' in url:
                regex_express = 'html\?movieid=(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    return 'http://vip.kankan.com/vod/%s.html' % match_result
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027
            #http://m.kankan.com/v/70/70763.shtml?subid=303027

            #http://vip.kankan.com/vod/84870.html
            #http://m.vip.kankan.com/play.html?movieid=84870
            if 'vod.kankan.com' in url:
                return url.replace('vod.kankan.com', 'm.kankan.com')
            elif 'vip.kankan.com' in url:
                regex_express = '(\d+)\.html'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    return 'http://m.vip.kankan.com/play.html?movieid=%s' % match_result
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.kankan.com/v/70/70763.shtml?subid=303027
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027

            #http://m.vip.kankan.com/play.html?movieid=84870
            #http://vip.kankan.com/vod/84870.html
            if 'm.kankan.com' in url:
                return url.replace('m.kankan.com', 'vod.kankan.com')
            elif 'm.vip.kankan.com' in url:
                regex_express = 'html\?movieid=(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    return 'http://vip.kankan.com/vod/%s.html' % match_result
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027
            #http://m.kankan.com/v/70/70763.shtml?subid=303027

            #http://vip.kankan.com/vod/84870.html
            #http://m.vip.kankan.com/play.html?movieid=84870
            if 'vod.kankan.com' in url:
                return url.replace('vod.kankan.com', 'm.kankan.com')
            elif 'vip.kankan.com' in url:
                regex_express = '(\d+)\.html'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    return 'http://m.vip.kankan.com/play.html?movieid=%s' % match_result
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.kankan.com/v/70/70763.shtml?subid=303027
            #http://vod.kankan.com/v/70/70763.shtml?subid=303027

            #http://m.vip.kankan.com/play.html?movieid=84870
            #http://vip.kankan.com/vod/84870.html
            if 'm.kankan.com' in url:
                return url.replace('m.kankan.com', 'vod.kankan.com')
            elif 'm.vip.kankan.com' in url:
                regex_express = 'html\?movieid=(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    match_result = match_result.groups()[0]
                    return 'http://vip.kankan.com/vod/%s.html' % match_result
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CHunantvConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            #留下一个问题：apad -> web -> ipad，会出现，ipad, web都变成了apad的地址了，而不会出现真实的地址
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            #留下一个问题：apad -> web -> ipad，会出现，ipad, web都变成了apad的地址了，而不会出现真实的地址
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            #http://m.hunantv.com/#/play/1123577
            regex_express = '(\d+)\.html'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(url)
            if match_result:
                match_result = match_result.groups()[0]
                return 'http://m.hunantv.com/#/play/%s' % match_result 
            else:
                '''由于aphone -> web -> apad是，web地址不是真实的web地址'''
                regex_express = 'play/(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    '''
    由于iphone转web时需要剧集号，而iphone的URL无法提供，所以无法转换，原样返回
    '''
    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hunantv.com/#/play/1123577
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            #http://m.hunantv.com/#/play/1123577
            regex_express = '(\d+)\.html'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(url)
            if match_result:
                match_result = match_result.groups()[0]
                return 'http://m.hunantv.com/#/play/%s' % match_result 
            else:
                '''由于aphone -> web -> apad是，web地址不是真实的web地址'''
                regex_express = 'play/(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    '''
    由于apad转web时需要剧集号，而apad的URL无法提供，所以无法转换，原样返回
    '''
    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hunantv.com/#/play/1123577
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            #http://m.hunantv.com/#/play/1123577
            regex_express = '(\d+)\.html'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(url)
            if match_result:
                match_result = match_result.groups()[0]
                return 'http://m.hunantv.com/#/play/%s' % match_result 
            else:
                '''由于aphone -> web -> apad是，web地址不是真实的web地址'''
                regex_express = 'play/(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    '''
    由于aphone转web时需要剧集号，而aphone的URL无法提供，所以无法转换，原样返回
    '''
    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hunantv.com/#/play/1123577
            #http://www.hunantv.com/v/5/51054/f/1123577.html
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CBaofengConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.baofeng.com/play/19/play-787519.html
            #http://m.hd.baofeng.com/play/19/play-787519.html

            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('www.baofeng.com', 'm.hd.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hd.baofeng.com/play/19/play-787519.html
            #http://www.baofeng.com/play/19/play-787519.html

            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('m.hd.baofeng.com', 'www.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.baofeng.com/play/19/play-787519.html
            #http://m.hd.baofeng.com/play/19/play-787519.html

            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('www.baofeng.com', 'm.hd.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hd.baofeng.com/play/19/play-787519.html
            #http://www.baofeng.com/play/19/play-787519.html

            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('m.hd.baofeng.com', 'www.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.baofeng.com/play/19/play-787519.html
            #http://m.hd.baofeng.com/play/19/play-787519.html

            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('www.baofeng.com', 'm.hd.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hd.baofeng.com/play/19/play-787519.html
            #http://www.baofeng.com/play/19/play-787519.html

            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('m.hd.baofeng.com', 'www.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.baofeng.com/play/19/play-787519.html
            #http://m.hd.baofeng.com/play/19/play-787519.html

            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('www.baofeng.com', 'm.hd.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.hd.baofeng.com/play/19/play-787519.html
            #http://www.baofeng.com/play/19/play-787519.html

            #http://m.hd.baofeng.com/play/0/play-241500-drama-1.html
            #http://www.baofeng.com/play/0/play-241500-drama-1.html
            return url.replace('m.hd.baofeng.com', 'www.baofeng.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            
class C1905Converter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CWasuConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/Play/show/id/5807214
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/Play/show/id/5807214
            return url
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/Play/show/id/5807214
            #http://www.wasu.cn/wap/Play/show/id/5807214
            return url.replace('www.wasu.cn', 'www.wasu.cn/wap')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/wap/Play/show/id/5807214
            #http://www.wasu.cn/Play/show/id/5807214
            return url.replace('www.wasu.cn/wap', 'www.wasu.cn')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/Play/show/id/5807214
            #http://www.wasu.cn/wap/Play/show/id/5807214
            return url.replace('www.wasu.cn', 'www.wasu.cn/wap')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/wap/Play/show/id/5807214
            #http://www.wasu.cn/Play/show/id/5807214
            return url.replace('www.wasu.cn/wap', 'www.wasu.cn')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/Play/show/id/5807214
            #http://www.wasu.cn/wap/Play/show/id/5807214
            return url.replace('www.wasu.cn/Play', 'www.wasu.cn/wap/Play')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://www.wasu.cn/wap/Play/show/id/5807214
            #http://www.wasu.cn/Play/show/id/5807214
            return url.replace('www.wasu.cn/wap', 'www.wasu.cn')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class CPptvConverter(BaseConverter):
    def __init__(self):
        pass

    def conv_web_to_ipad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('v.pptv.com', 'm.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_ipad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('m.pptv.com', 'v.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_iphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('v.pptv.com', 'm.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_iphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('m.pptv.com', 'v.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_apad(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('v.pptv.com', 'm.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_apad_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('m.pptv.com', 'v.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_web_to_aphone(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('v.pptv.com', 'm.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def conv_aphone_to_web(self, url):
        try:
            #log.app_log.info('%s : %s' % (self.__class__.__name__, url))
            #http://m.pptv.com/show/suvUUrogkM4xrxc.html
            #http://v.pptv.com/show/suvUUrogkM4xrxc.html
            return url.replace('m.pptv.com', 'v.pptv.com')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":
    import common.converter as converter
    urls = {
        #'youku':'http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html', 
        #'tudou':'http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html', 
        #'qq':'http://v.qq.com/cover/0/01ga9d6hkd9r4d9.html', 
        #'sohu':'http://tv.sohu.com/20150513/n412986358.shtml', 
        #'iqiyi':'http://www.iqiyi.com/v_19rrnnrs34.html', 
        'letv':'http://m.le.com/vplay_21768679.html', 
        #'1905':'http://www.1905.com/vod/play/623659.shtml', 
        #'kankan':'http://vod.kankan.com/v/70/70763.shtml?subid=303027', 
        #'hunantv':'http://www.hunantv.com/v/5/51054/f/1123577.html', 
        #'baofeng':'http://www.baofeng.com/play/19/play-787519.html', 
        #'wasu':'http://www.wasu.cn/Play/show/id/5807214', 
        #'pptv':'http://v.pptv.com/show/suvUUrogkM4xrxc.html', 
    }
    for (k, v) in urls.items():
        conv = 'C%sConverter' % k.capitalize()
        if hasattr(converter, conv):
            conv_handler = getattr(converter, conv)
            h = conv_handler()
            from_os = 'aphone'
            to_os = 'web'
            print '---------%s-----------' % to_os
            res = h.convert(v, from_os, to_os)
            print res
            print '---------%s-----------' % from_os
            res = h.convert(res, to_os, from_os)
            print res
