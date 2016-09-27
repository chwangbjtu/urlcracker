# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import sys
sys.path.append('.')
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload
from lxml import etree
import md5

class CBilibiliCracker(object):
    def __init__(self):
        self._httpcli = HttpDownload()
        self._format_map = {1: 'normal', 2: 'high', 3: 'super'}
    
    def build_url(self, cid, quality):
        # 老接口，用不了了
        # url = 'http://interface.bilibili.com/playurl?appkey=f3bb208b3d081dc8&cid=%s&quality=%s' % (cid, quality)
        # return url
        appkey = "85eb6835b0a1034e"
        secretkey = "2ad42749773c441109bdc0191257a664"
        m1 = md5.new()
        md5_str = "appkey=%s&cid=%s&quality=%s%s" % (appkey, cid, quality, secretkey)
        m1.update(md5_str)
        sign = m1.hexdigest()
        url = "http://interface.bilibili.com/playurl?appkey=%s&cid=%s&quality=%s&sign=%s" % (appkey, cid, quality, sign)
        return url
        
    def crack(self, para):
        result = {}
        try:
            cid = para['cid']
            segs = {}
            formats = []
            # 有bug，默认三种清晰度都有，其实可能会遇到没有的
            for i in self._format_map.keys():
                url = self.build_url(cid, i)
                resp = self._httpcli.get_data(url, timeout=5)
                if resp:
                    doc = etree.fromstring(resp)
                    seg = []
                    for node in doc.xpath("//video/durl"):
                        length_sel = node.xpath('./length/text()')
                        if length_sel:
                            duration = length_sel[0]
                        
                        url_sel = node.xpath('./url/text()')
                        if url_sel:
                            play_url = url_sel[0]    
                            if play_url:
                                seg.append({"url":play_url, "duration": str(int(duration) /1000 if duration else '')})
                                segs[self._format_map[i]] = seg
                                formats.append(self._format_map[i])

            if segs:
                result["format"] = formats
                result["seg"] = segs
                result["type"] = ParseType.DIRECT
                result["start"] = ""
                result["end"] = ""
            
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result
        
if __name__ == '__main__':
    cracker = CBilibiliCracker()
    para = {'cid':'9482158', 'aid':'4291092'}
    res = cracker.crack(para)
    print json.dumps(res)
    
    
