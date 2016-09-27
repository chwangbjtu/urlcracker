# -*- coding:utf-8 -*- 
import time
import traceback
from tornado import log
from hashlib import md5
from base64 import b64decode, b64encode
from lxml import etree
import urllib2
import re

import sys
sys.path.append('.')

from common.http_client import HttpDownload
from common.util import ErrorCode, ParseType
from common.converter import CWasuConverter

class CWasuCracker(object):
    def __init__(self):
        self._wkey_patterns = [re.compile('\'key\'\s+:\s+\'(\w+)\''), re.compile('_playKey = \'([a-zA-Z0-9+/=]+)\',')]
        self._ua = 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36'
        self._xml_url = "http://www.wasu.cn/Api/getPlayInfoById/id/%s/datatype/xml" 
        self._enc_url = "http://www.wasu.cn/Api/getVideoUrl/id/%s/key/%s?url=%s"
        self._httpcli = HttpDownload()
        self._hdd = {'hd0':'normal', 'hd1':'high', 'hd2':'super'}
        self._wasuc =  CWasuConverter()

    def crack(self, para):
        result = {}
        try:
            wid = para.get('wid')
            url = para.get('url')
            os = para.get('os')
            aurl = self.get_aurl(url, os)
            wkey = self.get_wkey(aurl)
            xurl = self._xml_url % wid
            sxml = self._httpcli.get_data(xurl)
            xml = etree.fromstring(sxml)
            segs_new = {}
            format_new = []
            segs_old = {}
            format_old = []
            for ele in xml.iter('mp4', 'video'):
                if ele.tag == 'mp4':
                    for hd in ele.iter('hd0', 'hd1', 'hd2'):
                        ft = self.get_format(hd.tag)
                        b64url = hd.text
                        encurl = self.get_encurl(wid, wkey, b64url)
                        if not encurl or re.match('http:.*.mp4', encurl):
                            continue
                        try:
                            decurl = self.get_decurl(encurl)
                            if decurl:
                                decurl += "?version=SWFPlayer_V.4.1.0&vid=%s" %wid
                        except Exception, e:
                            continue
                        segs_new[ft] = [{'url':decurl, 'duration':''}]
                        format_new.append(ft)
                elif ele.tag == 'video':
                    b64url = ele.text
                    encurl = self.get_encurl(wid, wkey, b64url)
                    if not encurl or re.match('http:.*.mp4', encurl):
                        continue
                    try:
                        decurl = self.get_decurl(encurl)
                        if decurl:
                            decurl += "?version=SWFPlayer_V.4.1.0&vid=%s" %wid
                    except Exception, e:
                        continue
                    ft = self.get_format(self.get_hd(xml.xpath("//bitrate/text()")[0]))
                    segs_old[ft] = [{'url':decurl, 'duration':''}]
                    format_old.append(ft)

            if format_new:
                result['format'] = format_new
                result['seg'] = segs_new
                result['start'] = ''
                result['end'] = ''
                result['type'] = ParseType.DIRECT
            elif format_old:
                result['format'] = format_old
                result['seg'] = segs_old
                result['start'] = ''
                result['end'] = ''
                result['type'] = ParseType.DIRECT
            else:
                result = {'error':1, 'code':ErrorCode.NO_RESPONSE}
        except Exception,e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result

    def get_format(self, hd):
        return self._hdd.get(hd)

    def get_hd(self, bitrate):
        if type(bitrate) != int:
            bitrate = int(bitrate)
        if bitrate >= 650000:
            hd = 'hd2'
        elif bitrate <= 350000:
            hd = 'hd0'
        else:
            hd = 'hd1'
        return hd

    def get_aurl(self, url, os):
        res_url = url
        try:
            if hasattr(self._wasuc, 'convert'):
                convert = getattr(self._wasuc, 'convert')
                cwurl = convert(url, os, 'web')
                if cwurl:
                    caurl = convert(cwurl, 'web', 'aphone')
                    if caurl:
                        res_url = caurl
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res_url

    def get_wkey(self, url):
        wkey = ''
        try:
            data = self._httpcli.get_data(url, self._ua, timeout=4)
            if data:
                for wkey_pattern in self._wkey_patterns:
                    m = wkey_pattern.search(data)
                    if m:
                        wkey = m.groups()[0]
                        break
        except Exception,e:
            pass
        finally:
            return wkey

    def get_encurl(self, wid, wkey, b64url):
        eurl = self._enc_url % (wid, wkey, b64url)
        xml = self._httpcli.get_data(eurl)
        encurl = ''
        try:
            evideo = etree.fromstring(xml).xpath('//video')
            if evideo:
                encurl = evideo[0].text
        except Exception,e:
            pass
        finally:
            return encurl

    def get_decurl(self, url):
        key = "wasu!@#48217#$@#1"
        operation = "DECODE"
        expire = 86400
        decurl = streamAuth(string=url, key=key, operation=operation, expire=expire)
        return decurl

def streamAuth(string, key, operation, expire):
    """
    string: 加密/解密字符串
    key: 秘钥
    operation: 加密/解密 ENCODE/DECODE
    expire: 生存期
    """
    ckey_length = 4
    key = md5(key == "" and "12345678" or key).hexdigest()
    keya = md5(key[0:16]).hexdigest()
    keyb = md5(key[16:32]).hexdigest()
    keyc = ckey_length > 0 and (operation == "DECODE" and string[0: ckey_length] or md5(str(int(time.time()))).hexdigest()[-ckey_length:]) or ""
    cryptkey = keya + md5(keya + keyc).hexdigest()
    key_length = len(cryptkey)
    string = operation == "DECODE" and b64decode(string[ckey_length:]) or "%s%s%s" % (expire > 0 and expire + int(time.time()) or '0000000000', md5(string + keyb).hexdigest()[0:16], string)
    string_length = len(string)
    result = ''
    box = range(128)
    rndkey = []
    for i in range(128):
        rndkey.append(ord(cryptkey[i % key_length]))
    i = j = 0
    for i in range(128):
        j = (j + box[i] + rndkey[i] ) % 128
        box[i], box[j] = box[j], box[i]
    a = i = j = 0
    for i in range(string_length):
        a = (a + 1) % 128
        j = (j + box[a]) % 128
        box[a], box[j] = box[j], box[a]
        result += chr(ord(string[i]) ^ box[(box[a] + box[j]) % 128])
    if operation == "DECODE":
        T1 = int(result[0:10])
        T2 = int(time.time())
        J1 = result[10:26]
        J2 = md5(result[26:] + keyb).hexdigest()[0:16]
        if T1 - T2 > 0 or T1 == 0 and J1 == J2:
            return result[26:]
        else:
            return ""
    else:
        return keyc + b64encode(result)


if __name__ == '__main__':
    import json
    para = {'url':"http://www.wasu.cn/wap/Play/show/id/6428315", 'wid':6428315}
    w = CWasuCracker()
    res = w.crack(para)
    print json.dumps(res)

