# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import re
import sys
sys.path.append('.')
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CV1Cracker(object):
    def __init__(self):
        self._httpcli = HttpDownload()

    def crack(self, para):
        result = {}
        try:
            url = self.convert_wurl_to_aurl(para['url'])
            res = self._httpcli.get_data(url)
            
            regex_express = 'source src=\"(.*\.(mp4))\"'
            regex_pattern = re.compile(regex_express)
            match_result = regex_pattern.search(res)
            if match_result:
                play_url = match_result.groups()[0]
                format = "normal"
                formats = []
                formats.append(format)
                
                segs = {}
                seg = []
                seg.append({"url":play_url, "duration": ""})
                segs[format] = seg
                
                if segs:
                    result["format"] = formats
                    result["seg"] = segs
                    result["type"] = ParseType.DIRECT
                    result["start"] = ""
                    result["end"] = ""
                    
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error':1, 'code':ErrorCode.UNKNOWN_ERROR}
        finally:
            return result
            
    def convert_wurl_to_aurl(self, url):
        return url.replace('www.v1.cn', 'm.v1.cn')
        
if __name__ == '__main__':
    cracker = CV1Cracker()
    para = {'duration' : 10, 'url': 'http://www.v1.cn/video/v_12841895.jhtml'}
    res = cracker.crack(para)
    print json.dumps(res)
    
    
