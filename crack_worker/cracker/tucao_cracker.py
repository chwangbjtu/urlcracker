# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import sys
import time
import urlparse
from lxml import etree
from cStringIO import StringIO
sys.path.append('.')
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CTucaoCracker(object):
    def __init__(self):
        self._httpcli = HttpDownload()
        self._format = 'high'
        
    def build_url(self, type, tvid):
        timestamp = int(time.time())
        #暂时发现服务器端没检查key
        key = "tucao4c35fe3d.cc"
        url = 'http://api.tucao.tv/api/playurl?type=%s&vid=%s&key=%s&r=%s' % (type, tvid, key, str(timestamp))
        return url
        
    def build_result(self, seg):
        result = {}
        segs = {}
        formats = []
        segs[self._format] = seg
        formats.append(self._format)
        result["format"] = formats
        result["seg"] = segs
        result["type"] = ParseType.DIRECT
        result["start"] = ""
        result["end"] = ""
        return result
        
    def crack(self, para):
        result = {}
        try:
            extra = para['extra']
            ret = urlparse.parse_qs(extra, True)
            if ret.get('file'):
                #有播放地址，直接返回
                seg = []
                seg.append({"url":ret['file'][0], "duration": ''})
                result = self.build_result(seg)
                return result

            type = ret['type'][0]
            tvid = ret['vid'][0]
            url = self.build_url(type, tvid)
            resp = self._httpcli.get_data(url, timeout=5)
            if resp:
                buffer = StringIO(resp)
                doc = etree.parse(buffer)
                seg = []
                for node in doc.xpath("//video/durl"):
                    duration = ''
                    play_url = ''
                    length_sel = node.xpath('./length/text()')
                    if length_sel:
                        duration = length_sel[0]
                    
                    url_sel = node.xpath('./url/text()')
                    if url_sel:
                        play_url = url_sel[0]
                        
                    if play_url:
                        seg.append({"url":play_url, "duration": str(int(duration) /1000)})
                        
                if seg:
                    result = self.build_result(seg)
                        
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result
            
if __name__ == '__main__':
    cracker = CTucaoCracker()
    para = {'extra':'type=video&file=http://mvvideo1.meitudata.com/56d9316d447433375.mp4'}
    res = cracker.crack(para)
    print json.dumps(res)
    