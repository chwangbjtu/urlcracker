# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json

import sys
sys.path.append('.')

from common.util import ErrorCode, ParseType

class CFakeCracker(object):

    def __init__(self):
        pass

    def crack(self, para):
        log.app_log.info('%s : %s' % (self.__class__.__name__, json.dumps(para)))
        result = {}
        try:
            url = para['url']
            vid = para['vid']
            cont_id = para['cont_id']

            result = {'url':url, 'type': ParseType.DIRECT, 'start':'', 'end':'', 'seg':{'high':[{'url': 'xxx', 'duration': 10}]}}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    fake = CFakeCracker()
    para = {'url': 'http://www.letv.com/ptv/vplay/23050060.html', 'vid': 2233, 'cont_id': 23050060}
    res = fake.crack(para)
    print json.dumps(res)
