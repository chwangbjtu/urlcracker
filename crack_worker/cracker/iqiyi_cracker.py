# -*- coding:utf-8 -*-
import traceback
from tornado import log
import sys
sys.path.append('.')
import cs

from driver.iqiyi_swf_driver import IqiyiSwfDriver
from driver.iqiyi_h5_driver import IqiyiH5Driver

class CIqiyiCracker(object):
    def __init__(self):
        driver_name = 'Iqiyi%sDriver' % cs.iqiyi_type.capitalize()
        self.driver = getattr(sys.modules[__name__], driver_name)()

    def crack(self, para):
        result = {}
        try:
            result = self.driver.parse(para)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result

if __name__ == '__main__':
    iqiyi = CIqiyiCracker()
    para = {'url': 'http://www.iqiyi.com/v_19rro2q4mg.html', 'vid': 2233, 'tvvid': 347655300,'ivid':"be63d714afd883b930f81679d9f05d5f", 'site':'iqiyi'}
    res = iqiyi.crack(para)
    import json
    print json.dumps(res)
