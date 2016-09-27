# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import sys
from lxml import etree
from cStringIO import StringIO
sys.path.append('.')
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CIfengCracker(object):
    def __init__(self):
        self._httpcli = HttpDownload()
        self._format_map = {'VideoPlayUrl': 'normal', 'VideoPlayUrlH': 'high'}
        self._format_map1 = {'350k': 'normal', '500k': 'high'}
        
    def build_url(self, guid):
        url = 'http://vxml.ifengimg.com/video_info_new/' + guid[34] + '/' + guid[34:] + '/' + guid + '.xml'
        return url

    def crack(self, para):
        result = {}
        try:
            guid = para['guid']
            url = self.build_url(guid)
            resp = self._httpcli.get_data(url, timeout=5)
            if resp:
                buffer = StringIO(resp)
                doc = etree.parse(buffer)
                segs = {}
                formats = []
                duration = ''
                duration_sel = doc.xpath('//PlayList/item/@Duration')
                if duration_sel:
                    duration = duration_sel[0]
                    
                nodes = doc.xpath('//PlayList/videos/video[@mediaType="mp4"]')
                if nodes:
                    for node in nodes:
                        seg = []
                        format_sel = node.xpath('./@bitrate')
                        url_sel = node.xpath('./@VideoPlayUrl')
                        if format_sel and url_sel:
                            format = self._format_map1[format_sel[0]]
                            seg.append({"url":url_sel[0], "duration": duration})
                            segs[format] = seg
                            formats.append(format)
                        
                else:
                    for af, ff in self._format_map.items():
                        url_sel = doc.xpath('//PlayList/item/@%s' % (af))
                        seg = []
                        if url_sel:
                            seg.append({"url":url_sel[0], "duration": duration})
                            segs[ff] = seg
                            formats.append(ff)
                        
                if segs:
                    result["format"] = formats
                    result["seg"] = segs
                    result["type"] = ParseType.DIRECT
                    result["start"] = ""
                    result["end"] = ""
        
        except Exception, e:
            print e
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result
            
if __name__ == '__main__':
    cracker = CIfengCracker()
    para = {'guid':'0166517b-29bb-4944-8cce-4b903f87f0a5'}
    res = cracker.crack(para)
    print json.dumps(res)
    
