# -*- coding:utf-8 -*- 
import traceback
from tornado import log
from lxml import etree

import sys
sys.path.append('.')

from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CPptvCracker(object):
    
    def __init__(self):
        self._api_url = "http://web-play.pptv.com/webplay3-0-%s.xml?version=4&type=web.fpp"
        self._real_url = "http://%s/%s/%s?fpp.ver=1.3.0.19&k=%s&type=web.fpp"
        self._all_format = ['fluent', 'high', 'super', 'original']
        #self._all_format = ['fluent', 'high', 'super', 'original', 'original_high']
        self._httpcli = HttpDownload()

    def crack(self, para):
        result = {}
        result['seg'] = {}
        format_list = result['format'] = []
        try:
            pptv_id = para.get('pptv_id', '')
            if pptv_id:
                api_url = self._api_url % pptv_id
                resp = self._httpcli.get_data(api_url)
                if resp:
                    doc = etree.fromstring(resp)
                    files = doc.xpath("//file/item[@rid and @bitrate and @height and @width and @ft]")
                    file_num = len(files)
                    for f in files:
                        df = f.attrib
                        rid = df.get('rid')
                        bitrate = df.get('bitrate')
                        ft = int(df.get('ft'))
                        if ft >= len(self._all_format):
                            continue
                        format = self._all_format[ft]
                        ipl = doc.xpath("//dt[@ft=%s]/sh" % ft)
                        ip = ipl[0].text if ipl else "vod.pplive.com.cust.footprint.net"
                        # 由于抓取到的IP可能是数字地址或域名不固定，统一采用域名
                        #ip = "vod.pplive.com.cust.footprint.net"
                        keyl = doc.xpath("//dt[@ft=%s]/key" % ft)
                        if not keyl:
                            continue
                        else:
                            key =keyl[0].text
                        sgml = doc.xpath("//dragdata[@ft=%s]/sgm[@no]" % ft)
                        l = []
                        for sgm in sgml:
                            dseg = sgm.attrib
                            real_url = self._real_url % (ip, dseg['no'], rid, key)
                            dur = dseg.get('dur', '')
                            #dur = str(int(float(dur)))
                            dur = str(dur)
                            l.append({'url': real_url, 'duration': dur})
                        
                        if not l:
                            continue

                        result['seg'][format] = l
                        format_list.append(format)

                    if not format_list:
                       result = {'error':1, 'code':ErrorCode.NO_RESPONSE}
                    else:
                        result['start'] = ''
                        result['end'] = ''
                        result['type'] = ParseType.DIRECT
                else:
                    result = {'error':1, 'code':ErrorCode.NO_RESPONSE}
            else:
                result = {'error':1, 'code':ErrorCode.PARAS_ERROR}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result

if __name__ == "__main__":
    import json
    para = {'url':"http://v.pptv.com/show/NBYCgOhOvvxf3UU.html", 'pptv_id': 23703319}
    p = CPptvCracker()
    res = p.crack(para)
    print json.dumps(res)
