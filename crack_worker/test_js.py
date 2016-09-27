# -*-coding:utf-8 -*-
import os
import PyV8
import json
import httplib
from urllib2 import urlparse
from tornado import log

from common.conf import Conf
from common.http_client import HttpDownload
from cracker.letv_cracker import LetvCracker
from cracker.youku_cracker import YoukuCracker

class XMLHttpRequest(PyV8.JSContext):

    def __init__(self):
        self.isSend=False
        self.callback=None

    def open(self, method, url):
        self.method = method.strip().upper()
        _,self.host,self.path,self.query,_=urlparse.urlsplit(url)

    def send(self, data=None):
        self.data = data
        self.isSend = True
        self._go()

    def get_onreadystatechange(self):
        pass

    def set_onreadystatechange(self, callback):
        self.callback = callback
        self._go()

    onreadystatechange = property(get_onreadystatechange, set_onreadystatechange)

    def _go(self):
        if self.isSend and self.callback:
            self.cnx = httplib.HTTPConnection(self.host)
            self.cnx.request(self.method, self.path + ("?"+self.query if self.query else ""),self.data)
            res = self.cnx.getresponse()
            self.readyState = 4
            self.status = res.status
            self.responseText = res.read(1000000)
            self.callback(self)

    def setRequestHeader(self, key, val):
        pass

class Test:

    def start(self):
        '''
        cracker = YoukuCracker()
        para = {'url': 'http://v.youku.com/v_show/id_XMTI1ODc5MjU2NA==.html', 'vid': 2233, 'yvid': "XMTI1ODc5MjU2NA==", 'site':'youku'}
        '''
        cracker = LetvCracker()
        para = {'url':'http://www.letv.com/ptv/vplay/21768679.html', 'cont_id':'21768679', 'site':'letv', 'vid':'12345'}
        result = cracker.crack(para)
        print '-----------cracker运行的结果----------'
        print result

        template_file = 'json2js.template' 
        template = self.read_file(template_file) 
        if not template:
            return

        with PyV8.JSContext() as ctxt:

            def get_js():
                http_client = HttpDownload()
                body = '{"vid": "letv","url": "http://www.letv.com/ptv/vplay/21768679.html","site": "letv","os": "web" }'
                url = 'http://192.168.16.113:8088/crack?parsestr=js'
                result = http_client.post_data(url, body)
                return result

            def format_js(result):
                js = template % json.dumps(result).replace('\\', '\\\\')
                return js

            def run_js(result):
                return ctxt.eval(result)      

            ctxt.locals.request = XMLHttpRequest()

            result = format_js(result) 
            print '-----------转换为js的结果----------'
            print result
            #result = get_js()
            #print '-----------获取到的js的结果----------'
            #print result
            result = run_js(result)
            print '-----------js运行的结果----------'
            print result

    def read_file(self, file):
        try:
            template_file = open(os.path.abspath('.') + '/' + file) 
            template_data = template_file.read()
            template_file.close()
            return template_data
        except Exception, e:
            print e

if __name__ == '__main__':

    test = Test()
    test.start()
