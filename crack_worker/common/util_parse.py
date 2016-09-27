#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import urllib2
import cookielib
import traceback
import sys
import gzip
from lxml import etree 
from cStringIO import StringIO
from tornado import log
sys.path.append('.')

from converter import CLetvConverter
from converter import CQqConverter
from converter import CHunantvConverter
from converter import CYoukuConverter
from converter import CIqiyiConverter
from converter import CSohuConverter
from converter import CPptvConverter
from converter import CWasuConverter
from converter import C1905Converter
from common.http_client import HttpDownload

user_agent_android = 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36'
user_agent_pc = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'

class Parser():

    def __init__(self):
        self.letvc = CLetvConverter()
        self.qqc = CQqConverter()
        self.hunantvc = CHunantvConverter()
        self.ykc = CYoukuConverter()
        self.iqiyic = CIqiyiConverter()
        self.sohuc = CSohuConverter()
        self.pptvc = CPptvConverter()
        self.wasuc = CWasuConverter()
        self.dy1905c = C1905Converter()
        self._httpcli = HttpDownload()

    def get_site(self,url):
        #r = re.compile('^.*://\w+\.(\w+).\w+/.*$')
        r = re.compile('^.*\.(\w+)\.(com|tv)/.*$')
        m = r.match(url)
        if not m:
            r = re.compile('^.*\.(\w+)\.cn/.*$')
            m = r.match(url)
        if m:
            return m.group(1)
        return ""
        
    def gunzip(res, data):
        inbuffer = StringIO(data)
        f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
        rdata = f.read()
        return rdata

    def parse_video_info(self, url, os):
        site = self.get_site(url)
        if site == "mgtv":
            site = "hunantv"
        elif site == "le":
            site = "letv"
        ret = {}
        if hasattr(self, 'parse_video_info_%s' % site):
            parse = getattr(self, 'parse_video_info_%s' % site)
            ret = parse(url, site, os)
        else:
            log.app_log.info('no support site:%s' % site)
        return ret
        
    def parse_video_info_ku6(self, url, site, os):
        result = {}
        try:
            regex_express ='/show/(.*).html'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(url)
            if match_result:
                match_result = match_result.groups()[0]
                result['svid']=match_result
            #patterns = {}
            #vid_patterns = [re.compile(', id:\s*"(\w+\.*)",')]
            #patterns['svid'] = vid_patterns
            #result = self.parse_video_info_base(url, site, patterns)
            
        except Exception, e:
            log.app_log.info("parse_video_info_ku6:", e)
        finally:
            return result

    def parse_video_info_56(self, url, site, os):
        result = {}
        try:
            patterns = {}
            vid_patterns = [re.compile('vid: \'(\d+)\',')]
            patterns['svid'] = vid_patterns
            result = self.parse_video_info_base(url, site, patterns)
            
        except Exception, e:
            log.app_log.info("parse_video_info_56:", e)
        finally:
            return result

    def parse_video_info_17173(self, url, site, os):
        result = {}
        try:
            patterns = {}
            vid_patterns = [re.compile('videoId: (\d+),')]
            patterns['videoId'] = vid_patterns
            result = self.parse_video_info_base(url, site, patterns)
            
        except Exception, e:
            log.app_log.info("parse_video_info_17173:", e)
        finally:
            return result
            
    def parse_video_info_acfun(self, url, site, os):
        result = {}
        try:
            patterns = {}
            vid_patterns = [re.compile('data-aid=\"(\w+)\"')]
            patterns['aid'] = vid_patterns
            result = self.parse_video_info_base(url, site, patterns)
        except Exception, e:
            log.app_log.info("parse_video_info_acfun:", e)
        finally:
            return result
            
    def parse_video_info_bilibili(self, url, site, os):
        result = {}
        try:
            data = self._httpcli.get_data(url, timeout=10)
            if not data:
                return result
            
            src = self.gunzip(data)
            if src:
                regex_express ='.*cid=(\w+)&aid=(\d+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(src)
                if match_result:
                    cid = match_result.groups()[0]
                    aid = match_result.groups()[1]
                    result['cid'] = cid
                    result['aid'] = aid
            
        except Exception, e:
            log.app_log.info("parse_video_info_bilibili:", e)
        finally:
            return result
            
    def parse_video_info_tucao(self, url, site, os):
        result = {}
        try:
            data = self._httpcli.get_data(url, timeout=10)
            if not data:
                return result
            
            if data:
                doc = etree.HTML(data)
                type_sel = doc.xpath('//ul[@id="player_code"]/li/text()')
                if type_sel:
                    type_vids = type_sel[0]
                    values = type_vids.split('|')
                    result['extra'] = values[0]
            
        except Exception, e:
            log.app_log.info("parse_video_info_tucao:", e)
        finally:
            return result
    
    def parse_video_info_ifeng(self, url, site, os):
        result = {}
        try:
            patterns = {}
            vid_patterns = [re.compile('\"id\": \"(.*)\"')]
            patterns['guid'] = vid_patterns
            result = self.parse_video_info_base(url, site, patterns)
        except Exception, e:
            log.app_log.info("parse_video_info_v1:", e)
        finally:
            return result
            
    def parse_video_info_v1(self, url, site, os):
        result = {}
        try:
            result['duration'] = 0
            
        except Exception, e:
            log.app_log.info("parse_video_info_v1:", e)
        finally:
            return result
        
    def parse_video_info_1905(self,url, site, os): 
        result = {}
        try:
            if hasattr(self.dy1905c, 'convert'):
                convert = getattr(self.dy1905c, 'convert')
                cwurl = None
                cwurl = convert(url, os, 'web')

                patterns = {}
                vid_patterns = [re.compile('mdbfilmid : \"(\d+)\"')]
                patterns['movieid'] = vid_patterns
                duration_patterns = [re.compile('play_duration:\"(\d+)\"')]
                patterns['duration'] = duration_patterns
              
                if cwurl:
                    result = self.parse_video_info_base(cwurl, site, patterns)
                else:
                    log.app_log.info("parse_video_info_1905:no caurl")
            else:
                log.app_log.info("parse_video_info_1905:no convert")
        except Exception, e:
            log.app_log.info("parse_video_info_1905:", e)
        finally:
            return result
                                
    def parse_video_info_hunantv(self,url, site, os): 
        result = {}
        try:
            if hasattr(self.hunantvc, 'convert'):
                convert = getattr(self.hunantvc, 'convert')
                cwurl = None
                caurl = None
                cwurl = convert(url, os, 'web')
                if cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                if caurl:
                    regex_express = r'play/(\d+)'
                    regex_pattern = re.compile(regex_express)
                    match_result = regex_pattern.search(caurl)
                    if match_result:
                        match_result = match_result.groups()[0]
                        result['cont_id'] = match_result
                        #result['url'] = caurl
                        #result['url'] = url
                    else:
                        log.app_log.info("parse_video_info_hunantv:no match_result")
                else:
                    log.app_log.info("parse_video_info_hunantv:no caurl")
            else:
                log.app_log.info("parse_video_info_hunantv:no convert")
        except Exception, e:
            log.app_log.info("parse_video_info_hunantv:", e)
        finally:
            return result

    def parse_video_info_letv(self,url, site,os): 
        result = {}
        try:
            if hasattr(self.letvc, 'convert'):
                convert = getattr(self.letvc, 'convert')
                cwurl = None
                caurl = None
            
                cwurl = convert(url, os, 'web')
                if cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                else:
                    log.app_log.info("parse_video_info_letv:no cwurl")
                regex_express = r'vplay_(\d+)'
                regex_pattern = re.compile(regex_express)
                if caurl:
                    match_result = regex_pattern.search(caurl)
                    if match_result:
                        match_result = match_result.groups()[0]
                        result['cont_id'] = match_result
                        #result['url'] = caurl
                        #result['url'] = url
                    else:
                        log.app_log.info("parse_video_info_letv:no match_result")
                else:
                    log.app_log.info("parse_video_info_letv: no caurl")
            else:
                log.app_log.info("parse_video_info_letv:no convert")
        except Exception, e:
            log.app_log.info("parse_video_info_letv:", e)
        finally:
            return result

    def parse_video_info_qq(self,url, site,os):
        result = {}
        try:
            #直接型:URL解析
            #http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63
            #二次型:解析网页内容获取
            #http://m.v.qq.com/cover/y/yaefxp2nxm03m2r.html
            #http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html
            caurl = None
            convter = getattr(self.qqc, 'conv_%s_to_web' % os)
            if convter:
                cwurl = convter(url)
                if cwurl:
                    caurl = self.iqiyic.conv_web_to_apad(cwurl)
                    url = caurl
            '''
            if 'm.v.qq.com' in url or 'v.qq.com' in url:
                regex_express = '\?vid=(\w+)'
                regex_pattern = re.compile(regex_express)
                match_result = regex_pattern.search(url)
                if match_result:
                    result['cont_id'] = match_result.groups()[0] 
                else:
                    result = self.parse_video_info_qq_second(url, site)
            elif 'film.qq.com' in url:
                result = self.parse_video_info_qq_second(url, site)
            '''
            result = self.parse_video_info_qq_second(url, site)
        except Exception, e:
            print e
        finally:
            return result

    def parse_video_info_qq_second(self,url, site):
        result = {}
        try:
            patterns = {}
            vid_patterns = [re.compile('\"vid\":\"(\w+|\d+)\"'),re.compile('vid:\"(\w+|\d+)\"')]
            #vid_patterns = [re.compile('\"id\":\"(\w+|\d+)\"'),re.compile('id :\"(\w+|\d+)\"')]
            patterns['vid'] = vid_patterns 
            result = self.parse_video_info_base(url, site, patterns)
        except Exception, e:
            print e
        finally:
            return result

    def parse_video_info_base(self,url, site, patterns):
        global user_agent_android
        result = {}
        try:
            ua = None
            if  site == 'pptv' or site == 'wasu':
                ua = user_agent_android
            if site == '1905' or site == 'qq' or site == '56' or site == 'iqiyi':       
                ua = user_agent_pc
            data = self._httpcli.get_data(url, ua, timeout=10)
            if not data:
                return result
            for (k, v) in patterns.items():
                for r in v:
                    m = r.search(data)
                    if m:
                        result[k] = m.groups()[0]
                        break
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result


    def parse_video_info_sohu(self,url, site,os):
        result = {}
        try:
            if hasattr(self.sohuc, 'convert'):
                convert = getattr(self.sohuc, 'convert')                
                cwurl = None
                cwurl = convert(url, os, 'web')
                patterns = {}
                vid_patterns = [re.compile('var vid=\"(\d+)\"'),re.compile('var vid = \'(\d+)\'')]
                patterns['svid'] = vid_patterns
                if cwurl:
                    result = self.parse_video_info_base(cwurl, site, patterns)
                    #if result:
                        #result['url'] = cwurl
                        #result['url'] = url
                else:
                    log.app_log.info("parse_video_info_sohu:no cwurl")
            else:
                log.app_log.info("parse_video_info_sohu:no convert")
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result

    def parse_video_info_pptv(self, url, site, os):
        result = {}
        try:
            if hasattr(self.pptvc, 'convert'):
                convert = getattr(self.pptvc, 'convert')
                cwurl = None
                caurl = None
                cwurl = convert(url, os, 'web')
                if cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                    patterns = {}
                    #pid_patterns = [re.compile('var webcfg = {\"id\":(\d+),')]
                    pid_patterns = [re.compile('\"channel_id\":(\d+),')]
                    patterns['pptv_id'] = pid_patterns
                    if caurl:
                        result = self.parse_video_info_base(caurl, site, patterns)
                        #if result:
                            #result['url'] = caurl
                            #result['url'] = url
                    else:
                        log.app_log.info("parse_video_info_pptv:no caurl")
                else:
                    log.app_log.info("parse_video_info_pptv:no cwurl")
            else:
                log.app_log.info("parse_video_info_pptv:no convert")
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result

    def parse_video_info_wasu(self, url, site, os):
        result = {}
        try:
            if hasattr(self.wasuc, 'convert'):
                convert = getattr(self.wasuc, 'convert')
                cwurl = None
                caurl = None
                cwurl = convert(url, os, 'web')
                if cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                    # 因为wkey会过期，改为在crack的时候再去获取，此处只获取wid
                    if caurl:
                        regex_pattern = re.compile(r'id/(\d+)')
                        match_result = regex_pattern.search(caurl)
                        if match_result:
                            result['wid'] = match_result.groups()[0]
                            #result['url'] = caurl
                            #result['url'] = url
                        else:
                            log.app_log.info("parse_video_info_wasu:no wid")
                    else:
                        log.app_log.info("parse_video_info_wasu:no caurl")
                    '''
                    patterns = {}
                    wkey_patterns = [re.compile('\'key\'\s+:\s+\'(\w+)\'')]
                    patterns['wkey'] = wkey_patterns
                    if caurl:
                        result = self.parse_video_info_base(caurl, site, patterns)
                        if result:
                            result['url'] = caurl
                            regex_pattern = re.compile(r'id/(\d+)')
                            match_result = regex_pattern.search(caurl)
                            if match_result:
                                result['wid'] = match_result.groups()[0]
                            else:
                                log.app_log.info("parse_video_info_wasu:no wid")
                        else:
                            log.app_log.info("parse_video_info_wasu:no wkey")
                    else:
                        log.app_log.info("parse_video_info_wasu:no caurl")
                    '''
                else:
                    log.app_log.info("parse_video_info_wasu:no cwurl")
            else:
                log.app_log.info("parse_video_info_wasu:no convert")
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result

    def parse_video_info_iqiyi(self,url, site,os):
        result = {}
        try:
            caurl = None
            convter = getattr(self.iqiyic, 'conv_%s_to_web' % os)
            if convter:
                cwurl = convter(url)
                if cwurl:
                    #caurl = self.iqiyic.conv_web_to_aphone(cwurl)
                    caurl = cwurl
                patterns = {}
                vid_patterns = [re.compile('Q\.PageInfo\.playInfo\.tvid[ ]?=[ ]?\"(\d+)\"[ ]?'),re.compile("data-player-tvid=\"(\d+)")]
                ivid_patterns = [re.compile('Q\.PageInfo\.playInfo\.vid[ ]?=[ ]?\"(\d|\w+)\"[ ]?'),re.compile("data-player-videoid=\"(\w+)\"")]
                patterns['tvvid'] = vid_patterns
                patterns['ivid'] = ivid_patterns
                if caurl:
                    result = self.parse_video_info_base(caurl, site, patterns)
        except Exception, e:
            print e
        finally:
            return result


    def parse_video_info_youku(self,url, site,os):
        result = {}
        try:
            if hasattr(self.ykc, 'convert'):
                convert = getattr(self.ykc, 'convert')
                #http://v.youku.com/v_show/id_XMTI5MjM1NzExMg==.html
                cwurl = None
                cwurl = convert(url, os, 'web')

                regex_express = r'id_(.*)\.html'
                regex_pattern = re.compile(regex_express)
                #match_result = regex_pattern.search(url)
                if cwurl:
                    match_result = regex_pattern.search(cwurl)
                    if match_result:
                        match_result = match_result.groups()[0]
                        if match_result:
                            result['yvid'] = match_result
                            #result['url'] = cwurl
                            #result['url'] = url
                else:
                    log.app_log.info("parse_video_info_youku:no cwurl")
            else:
                log.app_log.info("parse_video_info_youku:no convert")
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result

if __name__ == '__main__':

    #'''
    url = [
        "http://www.56.com/w50/play_album-aid-14294952_vid-MTM5OTEzODYx.html"
    ]
    #'''
    #url = [
    #    "http://v.youku.com/v_show/id_XODk0NTQ5MTcy.html?x",
    #    "http://www.tudou.com/albumplay/-4p1KhgF7Rs/R5vWaL1ZSvE.html",
    #    "http://m.v.qq.com/cover/y/yaefxp2nxm03m2r.html",
    #    "http://m.v.qq.com/cover/j/jwzfwv97k7xukzd.html?vid=z0016fa0l63",
    #    "http://film.qq.com/weixin/detail/2/2nh6bsl6mlxm7bf.html",
    #    "http://wx.m.tv.sohu.com/20150513/n412986358.shtml",
    #    "http://m.iqiyi.com/v_19rrnnrs34.html",
    #    "http://m.letv.com/vplay_22938315.html",
    #    "http://www.1905.com/vod/play/623659.shtml"
    #    "http://m.hunantv.com/#/play/1123577",
    #    "http://m.kankan.com/v/70/70763.shtml?subid=303027",
    #    "http://m.vip.kankan.com/play.html?movieid=84870",
    #    "http://m.hunantv.com/#/play/1123577",
    #    "http://m.hd.baofeng.com/play/19/play-787519.html",
    #    "http://www.wasu.cn/wap/Play/show/id/5807214",
    #    "http://m.pptv.com/show/suvUUrogkM4xrxc.html",
    #    "http://tv.sohu.com/20150428/n412012561.shtml",
    #    "http://m.iqiyi.com/v_19rrnqzz0k.html",
    #    "http://v.youku.com/v_show/id_XMTI5MjM1NzExMg==.html",
    #    "http://www.letv.com/ptv/vplay/21768679.html"
    #    "http://v.pptv.com/show/VyCwL1pXndsibvCQ.html",
        #"http://zt.pptv.com/show/2015/zxyx/index.html"
        #"http://www.wasu.cn/Play/show/id/306306"
    #    "http://www.1905.com/vod/play/346266.shtml"
    #]

    parser1 = Parser()
    '''
    for u in url:
        try:
            print u
            res = parser1.parse_video_info(u, "web")
            print res
        except Exception, e:
            print "exception: %s" %e
    '''
    print parser1.parse_video_info('http://www.acfun.tv/v/ac2701527', 'web')
    #print parser1.parse_video_info_iqiyi('http://www.iqiyi.com/v_19rro2aqds.html', 'iqiyi', 'web')
