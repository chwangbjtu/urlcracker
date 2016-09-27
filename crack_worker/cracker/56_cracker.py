# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import time
import sys
sys.path.append('.')
from uuid import uuid4
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload
reload(sys)
sys.setdefaultencoding('gb18030')
class C56Cracker(object):

    def __init__(self):
        self._httpcli = HttpDownload(with_cookie=True)
        self._url_action = "http://m.tv.sohu.com/phone_playinfo?vid=%s&site=2"
        self._url_list = "http://data.vod.itc.cn/cdnList?%s&vid=%s_2&prod=flash&rb=1"
        self._ua = "Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Safari/537.36"
        self._formats={"hig":"high","nor":"normal","sup":"super"}
    def get_action(self, vid):
        try:
            resp = self._httpcli.get_data(self._url_action % vid,ua=self._ua) 
            if resp:
                #return resp
                return json.loads(resp.decode().encode('utf8'))
        except Exception, e:
            print traceback.format_exc()
            #log.app_log.error(traceback.format_exc())

    def crack(self, para):
        result = {}
        try:
            vid = para['svid']
            res = self.get_action(vid)
            if "status" in res and "data" in res:
                if res["status"]==200:
                    data = res["data"]
                    if "urls" in data:
                        urls = data["urls"]
                        if "mp4" in urls:
                            mp4 = urls["mp4"]
                            seg = {}
                            format = []
                            for key in mp4:
                                if mp4[key] !=[]:
                                    list = mp4[key]
                                    seg[self._formats[key]]=[]
                                    format.append(self._formats[key])
                                    for item in list:
                                        item = item[item.find('?')+1:]
                                        item = item[:item.find('&')]
                                        url = self._url_list % (item,vid)
                                        r = self._httpcli.get_data(url)
                                        d = json.loads(r)
                                        tmp = {}
                                        tmp["url"]=d["url"]
                                        seg[self._formats[key]].append(tmp)
                                        #print d["url"]
                            if seg:
                                result["format"] = format
                                result["seg"] = seg
                                result["type"] = ParseType.DIRECT
                                result["start"] = ""
                                result["end"] = ""
                            else:
                                result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
                        else:
                            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
                    else:
                        result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
                else:
                    result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
            else:
                result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        except Exception, e:
            #log.app_log.error(traceback.format_exc())
            print traceback.format_exc()
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    cracker = C56Cracker()
    para = {'url': 'http://m.56.com/album/id-MTQzODE5NjY_vid-MTQwMzc3MzM1.html', 'vid':'1234', 'svid':'80533182', 'site':'sohu'}
    res = cracker.crack(para)
    print json.dumps(res)
