# -*- coding:utf-8 -*-
import re
import json
import traceback
from tornado import log
import sys
sys.path.append('.')
import urllib
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CHunantvCracker(object):
    
    def __init__(self):
        self._api_url = 'http://mobile.api.hunantv.com/v5/video/getSource?appVersion=4.6.7&osType=android&videoId=%s'
        self._httpcli = HttpDownload()

    def crack(self, para):
        result = {}
        try:
            if 'cont_id' in para:
                video_id = cont_id = para['cont_id']
                api_url = self._api_url % cont_id
                resp = self._httpcli.get_data(api_url)
                if resp:
                    segs = self.entrance_url_parse(resp)
                    if segs:
                        result['start'] = '"info":"'
                        result['end'] = '"'
                        result['seg'] = segs
                        result['format'] = segs.keys()
                        result['type'] = ParseType.CUSTOM
                    else:
                        result = {'error':1, 'code':ErrorCode.PARSE_ERROR}
                else:
                     result = {'error':1, 'code':ErrorCode.NO_RESPONSE}
            else:
                result = {'error':1, 'code':ErrorCode.PARAS_ERROR}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error':1, 'code':ErrorCode.UNKNOWN_ERROR}
        finally:
            return result 

    def entrance_url_parse(self, data):
        try:
            segs = {}
            json_data = json.loads(data) 
            #streams = json_data.get('data', {}).get('videoSources')
            streams = json_data.get('data', {}).get('shadowSources')
            #domains = json_data.get('data', {}).get('videoDomains')
            # 不分段，不处理duration
            #duration = json_data.get('info', {}).get('duration')
            #if streams and domains:
            if streams:
                #domain = domains[0]
                # segs = {'super':[{'url':'', 'duration':''}]}
                fd = {u'流畅': 'fluent', u'标清': 'normal', u'高清': 'high', u'超清': 'super'}
                for s in streams:
                    name = s.get('name')
                    url = s.get('url')
                    if name and url:
                        url = urllib.unquote(url)
                        #m3u8 = domain + url
                        # 访问一次，否则会出现405
                        #self._httpcli.get_data(m3u8)
                        #url = m3u8.replace('/playlist.m3u8','')
                        f = fd.get(name)
                        if f:
                            segs[f] = [{'url': url, 'duration': ''}]
            return segs
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == '__main__':
    cracker = CHunantvCracker() 
    # 电影
    #para = {'url':'http://www.mgtv.com/v/3/159507/f/2930137.html', 'cont_id':'2930137', 'site':'hunantv', 'vid':'12345'}
    # 电视剧
    #para = {'url':'http://www.mgtv.com/v/2/150514/f/3125969.html', 'cont_id':'3125969', 'site':'hunantv', 'vid':'12345'}
    # 综艺
    #para = {'url':'http://www.mgtv.com/v/1/18/f/3126057.html', 'cont_id':'3126057', 'site':'hunantv', 'vid':'12345'}
    # 小视频
    para = {'url':'http://www.hunantv.com/v/145/290486/f/3127659.html', 'cont_id':'3127659', 'site':'hunantv', 'vid':'12345'}
    # 动漫
    #para = {'url':'http://www.mgtv.com/v/7/292938/c/3125304.html', 'cont_id':'3125304', 'site':'hunantv', 'vid':'12345'}
    #para = {'url':'http://www.mgtv.com/v/2/157339/f/1768410.html', 'cont_id':'1768410', 'site':'hunantv', 'vid':'12345'}
    #para = {'url':'http://www.mgtv.com/v/3/158369/c/2973133.html', 'cont_id':'2973133', 'site':'hunantv', 'vid':'12345'}
    #para = {'url':'http://www.mgtv.com/v/3/108493/f/351667.html', 'cont_id':'1117556', 'site':'hunantv', 'vid':'12345'}
    #para = {'url':'http://www.hunantv.com/v/5/290541/f/3303960.html', 'cont_id':'3303960', 'site':'hunantv', 'vid':'12345'}
    res = cracker.crack(para)
    print json.dumps(res)
