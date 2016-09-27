# -*- coding:utf-8 -*-
import traceback
from tornado import log
import json
import os
import PyV8

import sys
sys.path.append('.')
from common.conf import Conf
from common.util import ErrorCode, ParseType
from common.http_client import HttpDownload

class YoukuCracker(object):

    def __init__(self):
        self._ctx = PyV8.JSContext()
        self._ctx.enter()
        self._httpcli = HttpDownload()
        #load js
        self._js = ""
        base_dir = os.path.abspath(".")
        filename = base_dir + "/js/youku.js"
        jsfile = open(filename)
        #jsfile = open('/tmp/crack_server/cracker/youku.js')
        try:
            self._js = jsfile.read( )
        finally:
            jsfile.close()

        self._func = self._ctx.eval(self._js)

    def crack(self, para):
        #log.app_log.info('%s : %s' % (self.__class__.__name__, json.dumps(para)))
        result = {}
        try:
            tvid = para['yvid']

            turl = "http://v.youku.com/player/getPlayList/VideoIDS/" + tvid + "/Pf/4/ctype/12/ev/1"
            resp = self._httpcli.get_data(turl)
            if resp:
                tjresp = json.loads(resp)
                jresp = tjresp["data"][0]
                sjresp = json.dumps(jresp)
                #sjresp = json.dumps(tjresp["data"][0])

                res = self._func(sjresp)
                #print res
                res_list = res.split(",")
                type = ""
                urls_num = 0
                tnum = len(res_list)-2
                if tnum >= 1:
                    type = res_list[tnum]
                    urls_num = int(res_list[tnum+1])

                segs  = []
                if "segs" in jresp and type in jresp["segs"] and len(jresp["segs"][type]) == int(urls_num):
                    i = 0
                    for i in range (urls_num):
                        seg = {}
                        seg["url"] = res_list[i]
                        seg["duration"] = str(jresp["segs"][type][i]["seconds"])
                        segs.append(seg)
                
                    #result["seg"] = {type:segs}
                    #result["format"]=[type]
                    result["seg"] = {'high':segs}
                    result["format"]=['high']
                    result["type"]=ParseType.DIRECT
                    result["start"]=""
                    result["end"]=""
        
            #print json.dumps(resp)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            result = {'error': 1, 'code': ErrorCode.NO_RESPONSE}
        finally:
            return result 

if __name__ == '__main__':
    youku = YoukuCracker()
    para = {'url': 'http://v.youku.com/v_show/id_XMTI1ODc5MjU2NA==.html', 'vid': 2233, 'yvid': "XMTI1ODc5MjU2NA==", 'site':'youku'}
    res = youku.crack(para)
    print json.dumps(res)
