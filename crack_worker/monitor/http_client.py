# -*- coding:utf-8 -*-
import urllib2
import cookielib
import traceback
import socket
 
import sys
sys.path.append('.')
from monitor.conf import Conf

def make_cookie(name, value):
        return cookielib.Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain="",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
        )

class HttpDownload(object):
    
    retry_times = 2;

    def __init__(self, with_cookie=False):

        self._opener = None
        self._cookies = None

        if with_cookie:
            self._cookies = cookielib.LWPCookieJar()
            handlers = [
                    urllib2.HTTPCookieProcessor(self._cookies)
            ]
            self._opener = urllib2.build_opener(*handlers)
        else:
            self._opener = urllib2.build_opener()

    def get_data(self, url, ua=None, cookies=None, timeout=10, read_body=True, read_all=False):
        if cookies:
            for c in cookies:
                self._cookies.set_cookie(make_cookie(c['name'], c['value']))
        req = urllib2.Request(url)
        if ua:
            req.add_header('User-Agent', ua)
        result = self._get_data(req, timeout, read_body, read_all)
        return result

    def _get_data(self, req, timeout, read_body, read_all, times=1):
        result = {'code':'', 'reason':'', 'length':'0', 'data':''}
        resp = None
        try:
            if times > self.retry_times:
                result['code'] = ''
                result['reason'] = 'timeout: retry %d times' % self.retry_times
                return result
            if timeout:
                resp = self._opener.open(req, timeout=timeout)
            else:
                resp = self._opener.open(req)
            content_length = resp.info().getheaders('Content-Length')
            if content_length:
                result['length'] = content_length[0]
            if read_body:
                data = ''
                if read_all:
                    chunk_size = 1024 * 1024
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        data += chunk
                else:
                    data = resp.read(Conf.http_read_size)
                result['data'] = data
            result['code'] = 200
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                result['code'] = str(e.code)
            if hasattr(e, 'reason'):
                result['reason'] = str(e.reason)
            if not result['code'] and not result['reason']:
                result['reason'] = '网络发生异常，urllib2未给code和reason'
        except socket.timeout as e:
            times = times + 1
            result = self._get_data(req, timeout, read_body, read_all, times) 
        finally:
            if resp:
                resp.close()
            return result

    def post_data(self, url, body, ua=None, cookies=None, timeout=10, read_body=True, read_all=False):
        if cookies:
            for c in cookies:
                self._cookies.set_cookie(make_cookie(c['name'], c['value']))
        req = urllib2.Request(url)
        if ua:
            req.add_header('User-Agent', ua)
        result = self._post_data(req, body, timeout, read_body, read_all)
        return result

    def _post_data(self, req, body, timeout, read_body, read_all, times=1):
        result = {'code':'', 'reason':'', 'length':'0', 'data':''}
        resp = None
        try:
            if times > self.retry_times:
                result['code'] = ''
                result['reason'] = 'timeout: retry %d times' % self.retry_times
                return result
            if timeout:
                resp = self._opener.open(req, body, timeout=timeout)
            else:
                resp = self._opener.open(req, body)
            content_length = resp.info().getheaders('Content-Length')
            if content_length:
                result['length'] = content_length[0]
            if read_body:
                data = ''
                if read_all:
                    chunk_size = 1024 * 1024
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        data += chunk
                else:
                    data = resp.read(Conf.http_read_size)
                result['data'] = data
            result['code'] = 200
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                result['code'] = str(e.code)
            if hasattr(e, 'reason'):
                result['reason'] = str(e.reason)
            if not result['code'] and not result['reason']:
                result['reason'] = '网络发生异常，urllib2未给code和reason'
        except socket.timeout as e:
            times = times + 1
            result = self._post_data(req, body, timeout, read_body, read_all, times) 
        finally:
            if resp:
                resp.close()
            return result


if __name__ == "__main__":
    import json
    hc = HttpDownload(with_cookie=True)
    body = {"vid":"23270427","url":"http://www.letv.com/ptv/vplay/23270427.html","os":"web","site":"letv"}
    data = json.dumps(body)
    res = hc.post_data('http://111.161.35.199:7410/crack', body=data, read_body=True)
    #res = hc.get_data('http://www.baidu.com')
    print 'length'
    print res['length']
    print 'data'
    print res['data']
    print 'code'
    print res['code']
    print 'reason'
    print res['reason']
