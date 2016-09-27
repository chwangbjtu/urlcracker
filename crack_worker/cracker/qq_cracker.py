# -*- coding:utf-8 -*-
import json
import traceback
from tornado import log
from driver.qq_phantomjs_driver import qqPhantomjsDriver

import sys
sys.path.append('.')

import cs
from common.util import ErrorCode

class CQqCracker(object):
    def __init__(self):
        driver_name = 'qq%sDriver' % cs.driver_type.capitalize()
        #self.driver = getattr(sys.modules[__name__], driver_name)(cs.apache_host, cs.apache_port, cs.gost_wait_timeout)
        self.driver = qqPhantomjsDriver(cs.apache_host, cs.apache_port, cs.qq_driver_timeout)
    def crack(self, para):
        result = {}
        try:
            #print para
            #result={'error': 1, 'code':10}
            vid = para['vid']
            response = self.driver.parse(vid)
            if not response:
                result = {'error': 1, 'code': ErrorCode.PARSE_ERROR}
            else:
                result = json.loads(response)
                if "error" in result:
                    result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
             
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    cracker = CQqCracker()
    para = {'url': 'http://film.qq.com/cover/r/rbg9e93w492s0c4.html', 'vid': "a0016axoclg", 'yvid': "b0017ejsi8c", 'site':'youku'}
    res = cracker.crack(para)
    print json.dumps(res)
