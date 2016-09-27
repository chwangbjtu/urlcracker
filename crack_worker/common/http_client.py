# -*- coding:utf-8 -*-
from tornado import httpclient
from tornado import log
import sys
sys.path.append('.')
import traceback
import json
import urllib2
import cookielib
import random
 
class HttpDownload(object):

    def __init__(self, with_cookie=False):
        self._opener = None
        self._cookies = None
        if with_cookie:
            self._cookies = cookielib.LWPCookieJar()
            handlers = [
                    #urllib2.HTTPHandler(debuglevel=1),
                    #urllib2.HTTPSHandler(debuglevel=1),
                    urllib2.HTTPCookieProcessor(self._cookies)
            ]
            self._opener = urllib2.build_opener(*handlers)
        else:
            self._opener = urllib2.build_opener()

    def make_cookie(self, name, value):
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

    def get_data(self, url, ua=None, cookies=None, timeout=1, headers = None):
        data = ''
        try:
            if cookies:
                for c in cookies:
                    self._cookies.set_cookie(self.make_cookie(c['name'], c['value']))
            req = urllib2.Request(url)
            if ua:
                req.add_header('User-Agent', ua)
            if headers:
                for k, v in headers.iteritems():
                    req.add_header(k, v)
            resp =  self._opener.open(req, timeout=timeout)
            chunk_size = 100 * 1024
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                data += chunk
            resp.close()
        except HTTPError as e:
            log.app_log.error('Error request [%s], code [%s]' % (url, e.code))
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return data

    def get_cookie(self):
        return ";".join(['%s=%s'%(c.name, c.value) for c in self._cookies])

    def post_data(self, url, body, ua=None, cookies=None, timeout=3):
        data = ''
        try:
            if cookies:
                for c in cookies:
                    self._cookies.set_cookie(self.make_cookie(c['name'], c['value']))
            req = urllib2.Request(url)
            if ua:
                req.add_header('User-Agent', ua)
            resp =  self._opener.open(req, body, timeout=timeout)
            chunk_size = 100 * 1024
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                data += chunk
            resp.close()
        except HTTPError as e:
            log.app_log.error('Error request [%s], code [%s]' % (url, e.code))
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return data

if __name__ == "__main__":

    hc = HttpDownload(with_cookie=True)
    hc.get_data('http://m.iqiyi.com/v_19rrlx9qto.html#vfrm=24-9-0-1')
    print hc.get_cookie() 
