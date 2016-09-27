# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json

import sys
sys.path.append('.')
import cs
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload
reload(sys)
sys.setdefaultencoding('utf-8')
class CSohuCracker(object):

    def __init__(self):
        self._httpcli = HttpDownload()
        self._format_vid = {"normal":"norVid", "high":"highVid", "super":"superVid", "original":"oriVid"}
        self._format_vid_linda = {"normal":"nor", "high":"hig", "super":"sup"}
        self._url_action = "http://hot.vrs.sohu.com/vrs_flash.action?vid=%s"
        self._url_real = "http://data.vod.itc.cn/?new=%s&mkey=%s&plat=17&prod=app"
        self._url_action_linda = "http://m.tv.sohu.com/phone_playinfo?vid=%s&site=%s&appid=tv&plat=17&sver=1.0"

    def get_action(self, vid,site=1):
        try:
            if site==2:
                resp = self._httpcli.get_data(self._url_action_linda % (vid,site))
                resp = resp.decode('gb2312').strip() 
            else:
                resp = self._httpcli.get_data(self._url_action % vid)
            if resp:
                return json.loads(resp)
        except Exception, e:
            print e
            print traceback.format_exc()
            #log.app_log.error(traceback.format_exc())

    def crack(self, para):
        #log.app_log.info('%s : %s' % (self.__class__.__name__, json.dumps(para)))
        result = {}
        try:
            segs = {}
            formats = []
            url =  para['url']
            if url.find('my.')!=-1:
                svid = para['svid']
                data = self.get_action(svid,2)['data']
                urls = data["urls"]
                mp4 = urls["mp4"]
                format_vid = {}
                for format, format_sohu in self._format_vid_linda.items():
                    if format_sohu in mp4 and mp4[format_sohu]:
                        format_vid[format] = mp4[format_sohu]
                
                for format, urls in format_vid.items():
                    seg = []
                    for url in urls:
                        new = url.find('new=')
                        new = url[new+4:]
                        new = new[:new.find('&')]
                        key = url.find('key=')
                        key = url[key+4:] 
                        key = key[:key.find('&')]
                        url_real = self._url_real % (new, key)
                        seg.append({"url":url_real})
                    if seg:
                        segs[format]=seg
                        formats.append(format)
            else:
                svid = para['svid']
                data = self.get_action(svid)['data']
                format_vid = {}
                for format, format_sohu in self._format_vid.items():
                    if format_sohu in data and data[format_sohu] != 0:
                        format_vid[format] = data[format_sohu]
                for format, fvid in format_vid.items():
                    res = self.get_action(fvid)
                    if not res:
                        continue
                    data = res.get('data', None)
                    if not data:
                        continue
                    durs = data.get("clipsDuration", [])
                    sus = data.get("su", [])
                    cks = data.get("ck", [])
                    len_durs = len(durs)
                    len_sus = len(sus)
                    len_cks = len(cks)
                    if 0 == len_sus or len_sus != len_cks or len_cks != len_durs:
                        continue
                    seg = []
                    for i in range(len_sus):
                        url_real = self._url_real % (sus[i], cks[i])
                        seg.append({"url":url_real, "duration": str(durs[i])})
                        #seg.append({"url":url_real, "duration": str(int(float(durs[i])))})
                    if seg:
                        segs[format] = seg
                        formats.append(format)

            if segs:
                result["format"] = formats
                result["seg"] = segs
                result["type"] = ParseType.DIRECT
                result["start"] = ""
                result["end"] = ""
            else:    
                result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    cracker = CSohuCracker()
    #para = {'url': 'http://my.tv.sohu.com/pl/8404262/83915045.shtml', 'vid':'1234', 'svid':'83915045', 'site':'sohu'}
    para = {'url': 'http://tv.sohu.com/20160530/n452055127.shtml', 'vid':'1234', 'svid':'3055570', 'site':'sohu'}
    res = cracker.crack(para)
    print json.dumps(res)
