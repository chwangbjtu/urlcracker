# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import time
import md5
import sys
sys.path.append('.')
from Crypto.Cipher import DES3
from urllib import urlencode
import base64
import random
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class C1905Cracker(object):
    def __init__(self):
        #self.init_headers()
        self._key = "iufles8787rewjk1qkq9dj76"
        self._iv = "vs0ld7w3"
        self._httpcli = HttpDownload()
        self._url_detail = "http://m.mapps.m1905.cn/Film/detail?id=%s"
        self._playurl = "http://m.mapps.m1905.cn/Film/filmPlayUrl?%s"
        self._register_url = "http://m.mapps.m1905.cn/Member/register"
        self._format_map = {"normal":"soonUrl", "high":"hdUrl", "super":"sdUrl"}
        
    def get_md5(self, str):
        m1 = md5.new()
        m1.update(str)
        return m1.hexdigest()
        
    def init_headers(self):
        self._headers = {}
        did = str(random.randint(100000000000000, 999999999999999))
        key = self.get_md5(did + 'm1905_2014')
        ua = 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36'
        self._headers = {'uid': '', 'sid': '', 'did': did, 'pid': '', 'ver': '100/46/2015071001', 'key': key, 'User-Agent': ua}
        #self.register_did()
        
    def encrypt_DES3_base64(self, message):
        cipher = DES3.new(self._key, DES3.MODE_CBC, self._iv)
        reminder = len(message) % 8 
        if reminder == 0:   #  pad 8 bytes 
            message += '\x08' * 8 
        else : 
            message += chr(8 - reminder) * (8 - reminder) 
            
        ciphertext = cipher.encrypt(message)
        result = base64.b64encode(ciphertext)
        return result
        
    def decrypt_base64_DES3(self, message):
        ciphertext = base64.b64decode(message)
        cipher = DES3.new(self._key, DES3.MODE_CBC, self._iv)
        plain = cipher.decrypt(ciphertext)
        return plain
        
    def register_did(self):
        try:
            url = self._register_url
            resp = self._httpcli.get_data(url, headers = self._headers)
            if resp:
                log.app_log.error("register_did error: %s" % (resp))
        
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        
    def get_detail(self, movie_id, index = 0):
        try:
            url = self._url_detail % movie_id
            resp = self._httpcli.get_data(url, headers = self._headers)
            if resp:
                details = json.loads(resp)
                if details['res']['result'] == 0:
                    return details
            
            else:
                return None
                
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            
    def get_playurl(self, playurl_obj):
        try:
            soonUrl = playurl_obj.get('soonUrl', '')
            hdUrl = playurl_obj.get('hdUrl', '')
            sdUrl = playurl_obj.get('sdUrl', '')
            argument = "soonUrl=" + soonUrl + "&hdUrl=" + hdUrl + "&sdUrl=" + sdUrl + "&type=1"
            encrypt_arg = self.encrypt_DES3_base64(argument)
            
            request = {}
            request['request'] = encrypt_arg
            encode_arg = urlencode(request)
            url = self._playurl % encode_arg
            resp = self._httpcli.get_data(url, headers = self._headers)
            if resp:
                plain = self.decrypt_base64_DES3(resp)
                plain = "".join([plain.rsplit("}" , 1)[0] , "}"]) 
                data = json.loads(plain)
                return data['data']
            else:
                return None
                
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        
    def crack(self, para):
        result = {}
        try:
            self.init_headers()
            if not para.has_key('movieid'):
                raise Exception("extra data has no key named movieid")
                
            movie_id = para['movieid']
            duration = para['duration']
            ret = self.get_detail(movie_id)
            if not ret:
                ret = self.get_detail(movie_id)
                if not ret:
                    raise Exception("no response from get detail api, movieid : %s, http headers : %s" % (movie_id, json.dumps(self._headers)))
                
            data = ret['data']
            playurls = data['playUrl']
            real_playurls = self.get_playurl(playurls)
            if not real_playurls:
                real_playurls = self.get_playurl(playurls)
                if not real_playurls:
                    raise Exception("no response from get url api, movieid : %s, http headers : %s" % (movie_id, json.dumps(self._headers)))
            
            format_url = {}
            for format, format_1905 in self._format_map.items():
                if format_1905 in real_playurls and real_playurls[format_1905] != "" and real_playurls[format_1905] != 0:
                    format_url[format] = real_playurls[format_1905]
            
            segs = {}
            formats = []            
            for format, playurl in format_url.items():    
                seg = []
                seg.append({"url":playurl, "duration": duration})
                if seg:
                    segs[format] = seg
                    formats.append(format)
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
    cracker = C1905Cracker()
    para = {'movieid':'2226299', 'duration': 10}
    res = cracker.crack(para)
    print json.dumps(res)
    
