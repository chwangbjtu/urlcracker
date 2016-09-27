# -*- coding:utf-8 -*-
import time
import md5
from Crypto.Cipher import AES
import base64
import urllib2
import json
from urllib import urlencode
from tornado import log
import traceback

import sys
sys.path.append('.')
from redis_mgr import RedisMgr
import cs
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class YoukuAppDriver(object):
    def __init__(self, host, port, timeout): 
        self._did = "02fcd60b280ca68dee0d0d8cb30be840"
        self._api_key = "qwer3as2jin4fdsa"
        self._format_map = {"normal":"3gphd", "high":{"flv":"flv","mp4":"mp4"},"super":"hd2"}
        self._details = {}
        self._redis = RedisMgr(cs.redis_ip, cs.redis_port, cs.redis_pwd)
        self._httpcli = HttpDownload()
        
        tmp_timeout = int(timeout / 1000)
        if tmp_timeout > 1:
            self._timeout = tmp_timeout
        else:
            self._timeout = 1
    
    #todo, wrap to lib
    def get_md5(self, str):
        m1 = md5.new()
        m1.update(str)
        return m1.hexdigest()
    
    #todo, wrap to lib    
    def decrypt_base64_AES(self, key, message):
        ciphertext = base64.b64decode(message)
        mode = AES.MODE_ECB
        decryptor = AES.new(key, mode)
        plain = decryptor.decrypt(ciphertext)
        return plain
        
    #todo, wrap to lib
    def encrypt_AES_base64(self, key, message):
        mode = AES.MODE_ECB
        encryptor = AES.new(key, mode)
        reminder = len(message) % 16 
        if reminder == 0:   #  pad 8 bytes 
            message += '\x08' *16 
        else : 
            message += chr(16 - reminder) * (16 - reminder) 
        encrypt_msg = encryptor.encrypt(message)
        result = base64.b64encode(encrypt_msg)
        return result
    
    #buid detail url
    def build_api_url(self, id):
        url = ''
        try:
            url_head = "http://a.play.api.3g.youku.com/common/v3/play?"
            time_str = str(int(time.time()))
            secret_seed = "GET:" + "/common/v3/play" + ":" + time_str + ":" + "631l1i1x3fv5vs2dxlj5v8x81jqfs2om"
            secret = self.get_md5(secret_seed)
            
            url_params = "_t_=" + time_str
            url_params += "&e=md5"
            url_params += "&_s_=" + secret
            const = "&format=1,2,3,4,5,6,7,8&language=default&did=" + self._did + "&ctype=20&local_point=115&audiolang=1&pid=0865e0628a79dfbb&guid=6351ae3e988fe1fc9c8be0a3e6960f64&mac=11:47:96:f4:67:27&imei=116614438598460&ver=4.8.1&operator=Android_46000&network=WIFI"
            url_params += "&point=1&id=" + id + "&local_time=0&local_vid=" + id  + const
            url = url_head + url_params
            
        except Exception, e:
            log.app_log.error("build api url error")
            log.app_log.error(traceback.format_exc())
        
        finally:
            return url 
        
    #def get detail from url, decrypt and return big json
    def get_api_data(self, url):
        try:
            content = self._httpcli.get_data(url, timeout=self._timeout)
            result_json = json.loads(content)
            
            if result_json.has_key('data'):
                data = result_json['data']
                src = self.decrypt_base64_AES(self._api_key, data)
                #print src
                self._details = json.loads(src)
            else:
                if result_json.has_key('err_desc'):
                    err_msg = result_json['err_desc']
                    log.app_log.error("get api data error, error msg: %s，url: %s" % (err_msg.encode("utf-8"), url.encode("utf-8")))
                else:
                    log.app_log.error("get api data error, error msg: 未知原因, url: %s" % (url))
            
        except Exception, e:
            log.app_log.error("get api data error, url: %s" % (url))
            log.app_log.error(traceback.format_exc())
    
    #build final url
    def get_final_url(self, url, field_id, token, oip, sid, gdid):
        final_url = ''
        try:
            src = sid + '_' + field_id + '_' + token
            ep = self.get_ep(src)
            if ep:
                final_url = url + "&oip=" + str(oip) + "&sid=" + sid + "&token=" + token + "&did=" + gdid + "&ev=1&ctype=20&" + ep
                
        except Exception, e:
            log.app_log.error("get final url error")
            
        finally:
            return final_url
        
    def get_ep(self, src):
        ep = ''
        try:
            redis_key = "youku:ep:key"
            ep_key = self._redis.get_data(redis_key)
            if not ep_key:
                log.app_log.error("youku:ep:key not exists")
            else:  
                encrypted_str = self.encrypt_AES_base64(ep_key, src)
                data = {'ep' : encrypted_str}
                ep = urlencode(data)
        
        except Exception, e:
            log.app_log.error("get ep error")
            log.app_log.error(traceback.format_exc())
            
        finally:
            return ep 
    
    def parse(self, vid):
        result_str = ''
        result = {}
        try:
            api_url = self.build_api_url(vid)
            if api_url:
                self.get_api_data(api_url)
                if self._details:
                    sid_data = self._details['sid_data']
                    token = sid_data['token']
                    oip = sid_data['oip']
                    sid = sid_data['sid']
                    results = self._details['results']
                    format_url = {}
                    for format, format_youku in self._format_map.items():
                        if format == "high":
                            d = {}
                            for k,v in format_youku.items():
                                if v in results and results[v] != "" and results[v] != 0:
                                    d[k]=results[v]
                            format_url[format] = d
                        elif format_youku in results and results[format_youku] != "" and results[format_youku] != 0:
                            format_url[format] = results[format_youku]
                    segs = {}
                    formats = []            
                    for format, fregments in format_url.items():    
                        seg = []
                        seg_high={}
                        if format == "high":
                            for k,v in fregments.items():
                                tmp=[]
                                for it in v:
                                    url = it['url']
                                    duration = str(it['seconds'])
                                    field_id = it['fileid']
                                    final_url = self.get_final_url(url, field_id, token, oip, sid, self._did)
                                    if final_url:
                                        tmp.append({"url":final_url, "duration": duration})
                                if tmp:
                                    seg_high[k]=tmp
                            if seg_high:
                                segs[format] = seg_high
                                formats.append(format)
                                    
                        else:
                            for freg in fregments:
                                url = freg['url']
                                duration = str(freg['seconds'])
                                field_id = freg['fileid']
                                final_url = self.get_final_url(url, field_id, token, oip, sid, self._did)
                                if final_url:
                                    seg.append({"url":final_url, "duration": duration})
                                
                            if seg:
                                segs[format] = seg
                                formats.append(format)
                            
                    if segs:
                        result["format"] = formats
                        result["seg"] = segs
                        result["type"] = ParseType.DIRECT
                        result["start"] = ""
                        result["end"] = ""
                        result_str = json.dumps(result)
            
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            
        finally:
            return result_str 
        
if __name__ == '__main__':
    cracker = YoukuAppDriver("localhost", 9999, 2000)
    res = cracker.parse('XMTQ2MTk3MjIxMg==')
    print res
    
