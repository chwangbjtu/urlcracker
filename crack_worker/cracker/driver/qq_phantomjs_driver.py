# -*- coding:utf-8 -*-
import re
import commands

class qqPhantomjsDriver(object):
    def __init__(self, host, port, timeout):
        self._phantomjs_file = './phantomjs/qq.js'
        self._flash_url = 'http://%s:%s/qq.html?id=%%s' % (host,port)
        self._phantomjs_cmd = 'phantomjs --load-plugins=%s %s %s' % ('true', self._phantomjs_file, timeout)
    
    def parse(self, vid):
        body = None
        url = self._flash_url % vid
        cmd = '%s %s' % (self._phantomjs_cmd, url)
        response = commands.getoutput(cmd)
        if response:
            regex_express = '<title>true</title>'
            regex_pattern = re.compile(regex_express)
            match_results = regex_pattern.search(response)
            if match_results:
                regex_express = '<body>(.*)</body>'
                regex_pattern = re.compile(regex_express)
                match_results = regex_pattern.search(response)
                if match_results:
                    body = match_results.groups()[0]
                    body = body.strip()
                    
        return body
        
if __name__ == "__main__":
    driver = qqPhantomjsDriver()
    res = driver.parse('XMTM0NTA5MTE5Mg==')
    #res = driver.parse('XMTI4MDEyMzEy')
    print res
    
