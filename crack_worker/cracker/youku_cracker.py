# -*- coding:utf-8 -*-
import json
import traceback
from tornado import log
#from driver.youku_ghost_driver import YoukuGhostDriver
from driver.youku_phantomjs_driver import YoukuPhantomjsDriver
from driver.youku_app_driver import YoukuAppDriver

import sys
sys.path.append('.')

import cs
from common.util import ErrorCode

class CYoukuCracker(object):
    def __init__(self):
        driver_name = 'Youku%sDriver' % cs.driver_type.capitalize()
        self.driver = getattr(sys.modules[__name__], driver_name)(cs.apache_host, cs.apache_port, cs.youku_driver_timeout)
            
    def crack(self, para):
        result = {}
        try:
            yvid = para['yvid']
            format = para['format'] if 'format' in para else None
            response = self.driver.parse(yvid)
            if not response:
                result = {'error': 1, 'code': ErrorCode.PARSE_ERROR}
            else:
                result = json.loads(response)
                if not format:
                    if "super" in result['format']:
                        result["format"].remove('super')
                        result['seg'].pop('super')
                    if 'high' in result['seg']:
                        high_url = result['seg']['high']
                        if 'mp4' in high_url and high_url['mp4']!="" and high_url['mp4']!=0:
                            result['seg']['high'] = high_url['mp4']
                        else:
                            result["format"].remove('high')
                            result['seg'].pop('high')
                else:
                    if 'high' in result['seg']:
                        high_url = result['seg']['high']
                        if 'mp4' in high_url and high_url['mp4']!="" and high_url['mp4']!=0:
                            result['seg']['high'] = high_url['mp4']
                        elif 'flv' in high_url and high_url['flv']!="" and high_url['flv']!=0:
                            result['seg']['high'] = high_url['flv']
                        else:
                            result["format"].remove('high')
                            result['seg'].pop('high')
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    cracker = CYoukuCracker()
    para = {'url': 'http://v.youku.com/v_show/id_XMTI4MDEyMzEy.html', 'vid': 348388906, 'yvid': "XMTI4MDEyMzEy", 'site':'youku','format':'all'}
    res = cracker.crack(para)
    print json.dumps(res)
