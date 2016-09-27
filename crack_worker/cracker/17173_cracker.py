# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import time
import sys
sys.path.append('.')
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class C17173Cracker(object):
    def __init__(self):
        self._httpcli = HttpDownload()
        self._format_map = {1:"normal", 2:"high", 4:"super"}

    def get_detail(self, video_id):
        result = None
        current = int(time.time() * 1000)
        url = "http://v.17173.com/api/video/vInfo/id/%s?t=%s" % (video_id, current)
        resp = self._httpcli.get_data(url)
        if resp:
            details = json.loads(resp)
            if details['success'] == 1:
                result =  details['data']['splitInfo']
        
        return result

    def crack(self, para):
        result = {}
        try:
            video_id = para['videoId']
            details = self.get_detail(video_id)
            formats = []
            segs = {}
            for detail in details:
                format_17173 = detail['def']
                format = self._format_map[format_17173]
                if not format:
                    log.app_log.error("unknown format: %s" % (format_17173))
                    
                formats.append(format)
                segs[format] = []
                infos = detail['info']
                for info in infos:
                    duration = info['duration']
                    url = info['url'][0]
                    segs[format].append({'url':url, 'duration':duration})
                    
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
    cracker = C17173Cracker()
    para = {'url': 'http://www.1905.com/vod/play/869029.shtml', 'vid':'875911', 'videoId':'31644528',  'duration': 10, 'site':'1905'}
    res = cracker.crack(para)
    print json.dumps(res)
    