# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import sys
import base64
import urllib
from Crypto.Cipher import ARC4
from urllib import quote
sys.path.append('.')
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class CAcfunCracker(object):
    def __init__(self):
        self._httpcli = HttpDownload()
        self._format_map = {'3gphd': 'normal', 'flv':'normal', 'flvhd':'high', 'mp4hd': 'high', 'mp4hd2':'super', 'mp4hd3':'original'}
        self.init()
        
    def init(self):
        # get vid, cover, title by content url, args need aid
        self._content_url = "http://api.aixifan.com/contents/%s"
        # get sourceId as video_id by plays url, args need vid
        self._plays_url = "http://api.aixifan.com/plays/%s"
        # get sign by custom url, args need video_id and refer
        self._custom_url = "https://api.youku.com/players/custom.json?type=h5&client_id=908a519d032263f8&video_id=%s&embsig=%s&%s"
        # youku get json url, args need sign
        self._youku_json_url = "http://play.youku.com/partner/get.json?vid=%s&ct=86&cid=908a519d032263f8&sign=%s"
        # refer,need by custom url, args need vid, cover, title
        self._refer = 'http://m.acfun.tv/ykplayer?date=undefined#vid=%s;cover=%s;title=%s&callback=ykv.callbacks.cb_AEFkYaN'
        self._headers = {}
        self._headers['deviceType'] = '2'
        # crack youku
        self._mk = {'a3':'1z4i','a4':'86rv'}
        self._user_cache = {'a1':'v','a2':'b'}
        # _rc4_decrypt_key get from _decrypt_seed
        self._rc4_decrypt_key = "10ehfkbv"
        # _rc4_encrypt_key get from _encrypt_seed
        self._rc4_encrypt_key = "msjv7h2b"
        type_3gphd = {'hd':1, 'key':'3gphd', 'loghd':4, 'play':True, 'quality':'mp4', 'suffix':'mp4'}
        type_flv = {'hd':0, 'key':'flv', 'loghd':0, 'play':False, 'quality':'flv', 'suffix':'flv'}
        type_flvhd = {'hd':0, 'key':'flvhd', 'loghd':0, 'play':False, 'quality':'flv', 'suffix':'flv'}
        type_mp4hd = {'hd':1, 'key':'mp4hd', 'loghd':1, 'play':True, 'quality':'mp4', 'suffix':'mp4'}
        type_mp4hd2 = {'hd':2, 'key':'mp4hd2', 'loghd':2, 'play':False, 'quality':'hd2', 'suffix':'flv'}
        type_mp4hd3 = {'hd':3, 'key':'mp4hd3', 'loghd':3, 'play':False, 'quality':'hd3', 'suffix':'flv'}
        self._stream_types = {'3gphd':type_3gphd, 'flv':type_flv, 'flvhd':type_flvhd, 'mp4hd':type_mp4hd, 'mp4hd2':type_mp4hd2, 'mp4hd3':type_mp4hd3}
        self._decrypt_seed = "1z4iogbv"
        self._encrypt_seed = "86rvailb"
        self._e = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]
            
    #not useful, we know rc4_key is always same
    def get_rc4_key(self, t):
        n = []
        i = 0
        length = len(t)
        while i < length:
            r = 0
            if t[i] >= 'a' and t[i] <= 'z':
                r = ord(t[i]) - ord('a')
            else:
                r = ord(t[i]) - ord('0') + 26
                
            o = 0
            while 36 > o:
                if self._e[o] == r:
                    r = o
                    break
                o += 1
            
            if r > 25:
                n.append(str(r - 26))
            else:
                n.append(chr(r + 97))
            i += 1
        return "".join(n)
        
    def get_sid_token(self, base64_str):
        msg = self.rc4_decrypt(base64_str)
        if msg:
            ret = msg.split('_')
            if len(ret) == 2:
                self._sid = ret[0]
                self._token = ret[1]
        
    def rc4_decrypt(self, base64_str):
        encrypt_str = base64.b64decode(base64_str)
        cipher = ARC4.new(self._rc4_decrypt_key)
        msg = cipher.decrypt(encrypt_str)
        return msg
        
    def rc4_encrypt(self, src):
        cipher = ARC4.new(self._rc4_encrypt_key)
        msg = cipher.encrypt(src)
        encrypt_str = base64.b64encode(msg)
        return encrypt_str
        
    def get_field_id(self, field_id, seg_num):
        i = field_id[0:8]
        r = self.get_hex_string(seg_num)
        o = field_id[10:]
        n = i + r + o
        return n
        
    def get_hex_string(self, seg_num):
        r = hex(seg_num)[2:]
        if len(r) == 1:
            r = '0' + r
        return r   
        
    def get_ep(self, field_id):
        src = self._sid + '_' + field_id + '_' + self._token
        #src = '846191191252886064b76_030020010056CF207CA72D2D9B7D2F958141AE-2EDF-6B01-E970-E557BC2CB3FB_7096'
        ep = self.rc4_encrypt(src)
        data = {'ep': ep}
        ep = urllib.urlencode(data)
        return ep
        
    def parse_path(self, s):
        n = ''
        for k, v in s.items():
            a = k + '/' + v + '/'
            n = a + n
            
        return n
        
    def build_params(self, u):
        e = []
        for k, v in u.items():
            n = k + '=' + str(v)
            e.append(n)
        return '&'.join(e)
    
    def get_mp4_src(self, s, u):
        i = self.parse_path(s)
        url = "http://k.youku.com/player/getFlvPath/" + i + self.build_params(u)
        return url
        
    def get_all_urls(self, streams):
        result = {}
        for stream in streams:
            stream_type = self._stream_types[stream['stream_type']]
            result[stream['stream_type']] = []
            st = stream_type['suffix']
            stream_field_id = stream['stream_fileid']
            segs = stream['segs']
            num = 0
            for seg in segs:
                key = seg['key']
                seconds = int(seg['total_milliseconds_video']) / 1000
                current_field_id = self.get_field_id(stream_field_id, num)
                sid = self._sid + '_' + self.get_hex_string(num)
                ep = self.get_ep(current_field_id)
                ep = ep[3:]
                
                s = {'sid':sid, 'fileid':current_field_id, 'st':st}
                u = {'K':key, 'hd':stream_type['hd'], 'myp':0, 'ts': seconds, 'ypp':0, 'ep':ep, 'ctype':'86', 'ev':1, 'token':self._token, 'oip':self._oip}
                url = self.get_mp4_src(s, u)
                result[stream['stream_type']].append({"url":url, "duration": seconds})
                num += 1
                
        return result
        
    def crack(self, para):
        result = {}
        try:
            aid = para['aid']
            content_url = self._content_url % (aid)
            resp = self._httpcli.get_data(content_url, headers=self._headers, timeout=5)
            if resp:
                resp_json = json.loads(resp)
                # bug to do:里面有多个个video的，只取第一个
                vid = resp_json['data']['videos'][0]['videoId']
                cover = resp_json['data']['cover']
                title = resp_json['data']['title']
                plays_url = self._plays_url % (vid)
                resp = self._httpcli.get_data(plays_url, headers=self._headers, timeout=5)
                if resp:
                    resp_json = json.loads(resp)
                    video_id = resp_json['data']['sourceId']
                    embsig = resp_json['data']['embsig']
                    refer = self._refer % (vid, cover, title)
                    data = {'refer':refer.encode('UTF-8')}
                    urlencode_refer = urllib.urlencode(data)
                    custom_url = self._custom_url % (video_id, embsig, urlencode_refer)
                    resp = self._httpcli.get_data(custom_url, timeout=5)
                    if resp:
                        resp_json = json.loads(resp)
                        sign = resp_json['playsign']
                        youku_json_url = self._youku_json_url % (video_id, sign)
                        resp = self._httpcli.get_data(youku_json_url, timeout=5)
                        if resp:
                            resp_json = json.loads(resp)
                            encrypt_str = resp_json['data']['security']['encrypt_string']
                            self._oip = resp_json['data']['security']['ip']
                            self.get_sid_token(encrypt_str)
                            streams = resp_json['data']['stream']
                            urls = self.get_all_urls(streams)
                            formats = []
                            segs = {}
                            for k, v in urls.items():
                                format =  self._format_map[k]
                                if not format in formats:
                                    formats.append(format)
                                    segs[format] = v
                                    
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
    cracker = CAcfunCracker()
    para = {'aid':'3010603'}
    res = cracker.crack(para)
    print json.dumps(res)
    #print cracker.get_sid_token('J8JkLOSODq+HMz+kj7wSX5aJUJqEw2+eB3o=')
    #print cracker.get_rc4_key('86rvailb')
    #print cracker.get_field_id('030020010056CF207CA72D2D9B7D2F958141AE-2EDF-6B01-E970-E557BC2CB3FB', 0)
    #print cracker.get_ep('a')
    
    
