# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import re
import sys
sys.path.append('.')

from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CKu6Cracker(object):

    def __init__(self):
        self._httpcli = HttpDownload()
        self._url_action = "http://v.ku6.com/fetch.htm?t=getVideo4Player&vid=%s"
        self._url_real = "http://data.vod.itc.cn/?new=%s&mkey=%s&plat=17&prod=app"
        self._format = {u"流  畅":"fluent",u"标  清":"normal",u"高  清":"high",u"超  清":"super"}

    def get_action(self, vid):
        try:
            resp = self._httpcli.get_data(self._url_action % vid,timeout=5) 
            if resp:
                return json.loads(resp)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def crack(self, para):
        result = {}
        try:
            svid = para['svid']
            data = self.get_action(svid)['data']
            if u'f' in data:
                url = data[u'f']
                urls = url.split(',')
                url2 = urls[0]+"?start=0&ref=out"
                res = self._httpcli.get_data(url2,timeout=5)
                if res:
                    seg={}
                    formats=[]
                    data = json.loads(res)
                    format = data["RateInfo"]
                    format = set(format.split(';'))
                    for k in self._format:
                        for it in format:
                            if it.find(k)!=-1:
                                it = it.split('@')
                                l=[]
                                for item in urls:
                                    d={}
                                    d["url"]=item+"?rate="+it[0]
                                    l.append(d)
                                seg[self._format[k]]=l
                                formats.append(self._format[k])
                    if seg:
                        result["format"] = formats
                        result["seg"] = seg
                        result["type"] = ParseType.DIRECT
                        result["start"] = ""
                        result["end"] = ""
            else:
                log.app_log.error("video can not watch")
        except Exception, e:
            #log.app_log.error(traceback.format_exc())
            log.app_log.error("get_action return value error")
            #print traceback.format_exc()
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    cracker = CKu6Cracker()
    para = {'url': 'http://tv.sohu.com/20140522/n399900251.shtml', 'vid':'1234', 'svid':'JZyr4byzjqncaPT1-IEv5A..', 'site':'ku6'}
    res = cracker.crack(para)
    print json.dumps(res)
