# -*- coding:utf-8 -*-
import re
import os
import hashlib
import urllib2
import gzip
import StringIO
from math import floor
from uuid import uuid4
from random import random, randint

try:
    import simplejson as json
except ImportError:
    import json

import sys
sys.path.append('.')

import traceback
from tornado import log, options
import cs
from common.util import ErrorCode, ParseType
from redis_mgr import RedisMgr
#options.parse_config_file('cs.py')
from common.http_client import HttpDownload

class IqiyiSwfDriver(object):
    
    ua = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'
    
    def __init__(self, *args, **kwargs):
        self.b2f = {1:'fluent', 2:'high', 4:'super', 5:'original'}
        # self.salt = "6ab6d0280511493ba85594779759d4ed"
        self._redis = RedisMgr(cs.redis_ip, cs.redis_port, cs.redis_pwd)
        self._httpcli = HttpDownload()

    def parse(self, para):
        result = {}
        try:
            tvid = str(para.get('tvvid', ''))
            ivid = str(para.get('ivid', ''))
            # read from redis
            salt = self._redis.get_data(cs.iqiyi_salt_key)
            vms = self.get_vms(tvid, ivid, salt)
            #raw_info = self.http_down(vms)
            raw_info = self._httpcli.get_data(vms)
            if not raw_info:
                result = {'error': 1, 'code': ErrorCode.PARSE_ERROR}
            else:
                info = json.loads(raw_info)
                # 分解拼装
                prefix = info["data"]["vp"]["du"]
                vs = info["data"]["vp"]["tkl"][0]["vs"]
                segs = {}
                format_list = []
                for v in vs:
                    bid = v.get('bid', '')
                    if not bid in self.b2f.keys():
                        continue
                    ft = self.b2f[bid]
                    fs = v.get('fs', [])
                    seg = []
                    for f in fs:
                        tail = f.get('l', '')
                        if not tail.startswith('/'):
                           tail = self.decrypt_tail(tail)
                        if not tail:
                            continue
                        # 过滤掉vip
                        if tail.startswith('/vip'):
                            continue
                        url = prefix + tail
                        duration = str(f['d'] / 1000.0)
                        seg.append({'url':url ,'duration':duration})
                    if seg:
                        segs[ft] = seg
                        format_list.append(ft)
                if segs:
                    result['seg'] = segs
                    result['format'] = format_list
                    result['type'] = ParseType.CUSTOM
                    result['start'] = '"l":"'
                    result['end'] = '"'
                else:
                    result = {'error':1, 'code':ErrorCode.PARSE_ERROR}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result

    def get_vms(self, tvid, ivid, salt):
        # generate core parameter：tvid、ivid、tm、enc、qyid、authkey、tn
        vms_api = ("http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7&vinfo=1&puid=&um=0&pf=b6c13e26323c537d&thdk=&thdt=&rs=1&k_tag=1"
                   "&tvId={0}&vid={1}&tm={2}&enc={3}&qyid={4}&authkey={5}&tn={6}")
        tm = str(randint(2000,4000))
        enc = sc = hashlib.md5(salt + tm + tvid).hexdigest()
        qyid = uid = uuid4().hex
        authkey = hashlib.md5(hashlib.md5(b'').hexdigest()+str(tm)+tvid).hexdigest()
        tn = str(random())

        vms = vms_api.format(tvid, ivid, tm, enc, qyid, authkey, tn)
        return vms

    def http_down(self, url):
        httpdata = ''
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', self.ua)
            resp = urllib2.urlopen(req)
            httpdata = resp.read()
            if resp.headers.get('content-encoding', None) == 'gzip':
                httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
            charset = resp.headers.getparam('charset')
            resp.close()
            match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
            if match:
                charset = match[0]
            if charset:
                charset = charset.lower()
            if (charset != 'utf-8') and (charset != 'utf8'):
                httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return httpdata

    def decrypt_tail(self, vlink):
        res = ''
        try:
            loc6 = 0
            loc2 = ''
            loc3 = vlink.split("-")
            loc4 = len(loc3)

            for i in range(loc4-1, -1, -1):
                loc6 = self.getVRSXORCode(int(loc3[loc4-i-1],16),i)
                loc2 += chr(loc6)
            res = loc2[::-1]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def getVRSXORCode(self, arg1,arg2):
        loc3 = arg2%3
        if loc3 == 1:
            return arg1^121
        if loc3 == 2:
            return arg1^72
        return arg1^103

if __name__ == '__main__':
    isd = IqiyiSwfDriver()
    # para = {'url': 'http://www.iqiyi.com/v_19rro2q4mg.html', 'vid': 2233, 'tvvid': 347655300,'ivid':"be63d714afd883b930f81679d9f05d5f", 'site':'iqiyi'}
    para = {'url': 'http://vip.iqiyi.com/20110826/317fa181f30178ed.html', 'vid':2211, 'tvvid':119087, 'ivid':'989d420bdd26430c938d615c2a90eab2', 'site':'iqiyi'}
    res = isd.parse(para)
    print json.dumps(res)

    tail = "3e-4d-1-66-1c-53-79-4f-4-2c-4e-3-2b-4e-5f-71-40-6-29-4a-5e-70-4a-1-7c-4f-51-2b-41-51-78-1c-5-2c-1d-5f-67-4b-56-7a-48-54-79-49-55-67-f-48"
    de = isd.decrypt_tail(tail)
    print de
