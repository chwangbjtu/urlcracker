# -*-coding:utf-8 -*-
import time
import sys
import os
import pkgutil
import json
import traceback
from tornado import log
from multiprocessing import Process
import re
from hashlib import md5

from redis_mgr import RedisMgr, MultiRedisMgr
from common.util_parse import Parser
import cs
from tornado import options
options.parse_config_file('cs.py')

class CrackWorker(Process):
    def __init__(self):
        Process.__init__(self)
        self._interval = cs.worker_sleep_time 
        self._ttl = json.loads(cs.ttl)
        self._edd_ttl = cs.edd_ttl
        self._redis = RedisMgr(cs.redis_ip, cs.redis_port, cs.redis_pwd)
        self._multi_redis = MultiRedisMgr(cs.redis_node) if cs.redis_node_on else None

        self._cracker = {}
        self._os = {'web', 'ipad', 'iphone', 'apad', 'aphone'}
        self._parser = Parser()

        log.app_log.info("start crack_worker")

    def run(self):
        try:
            self.load_cracker()
            while True:
                task = self.get_task()
                if task:
                    log.app_log.debug("get tsak vid:%s, task BEGIN", task['vid'])
                    self.execute_task(task)
                else:
                    time.sleep(self._interval)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

               
    def load_cracker(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "cracker")
            modules = pkgutil.iter_modules(path=[path])
           
            for loader, mod_name, ispkg in modules:
                if mod_name == 'driver':
                    continue
                if mod_name not in sys.modules:
                    loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])
                    class_name = "".join([r.capitalize() for r in mod_name.split('_')])
                    class_name = 'C' + class_name
                    site = mod_name.split('_')[0]
                    loaded_class = getattr(loaded_mod, class_name)

                    self._cracker[site] = loaded_class()
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def get_task(self):
        try:
            task = self._redis.pop_data("crack:task:queue")
            if task:
                return json.loads(task)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def get_ttl(self, site):
        try:
            if site in self._ttl:
                return self._ttl[site]
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def get_key(self, mark, site, vid, url):
        try:
            result_key = ""
            r = re.compile("([^?]+).*")
            prune_url = r.match(url).group(1)
            result_key = "%s:%s:%s:%s" % (mark, site, vid, md5(prune_url).hexdigest())
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return result_key

    def execute_task(self, task):
        try:
            result = {}
            vid = task.get('vid', '')
            site = task.get('site', '')
            url = task.get('url', '')
            os = task.get('os', '')
            format = task.get('format','')
            if not vid:
                log.app_log.error("crack fail:vid is empty, task FAIL")
            elif not url:
                log.app_log.error("crack fail:url is empty for task vid:%s, task FAIL" % vid)
            elif os not in self._os:
                log.app_log.error("crack fail:no support os for task vid:%s, task FAIL" % vid)
            elif site not in self._cracker:
                log.app_log.error("crack fail:no support site for task vid:%s, task FAIL" % vid)
            else:
                # 缓存中获取破解需要的额外信息
                jpara = None
                dpara = {}
                extra_key = self.get_key("extra", site, vid, url)
                result_key = self.get_key("crack", site, vid, url)
                if not extra_key or not result_key:
                    log.app_log.error("crack fail:empty key, vid: %s, task FAIL" % vid)
                    return
                jpara = self._redis.get_data(extra_key)
                if not jpara and self._multi_redis:
                    jpara = self._multi_redis.get_data(extra_key)
                if not jpara:
                    # 获取破解需要的额外信息
                    log.app_log.debug("parse video info, url: %s, vid: %s" % (url, vid))
                    dpara = self._parser.parse_video_info(url, os)
                    if dpara:
                        log.app_log.debug("parse ok, vid: %s" % (vid, ))
                        jpara = json.dumps(dpara)
                        # 添加到redis中
                        self._redis.set_data(extra_key, jpara, self._edd_ttl)
                    else:
                        log.app_log.debug("parse failed, vid: %s" % (vid, ))
                else:
                    dpara = json.loads(jpara)
                if format:
                    dpara['format'] = format        
                # 获取到破解需要的额外信息，进行破解
                if dpara:
                    dpara['os'] = os
                    dpara['url'] = url
                    log.app_log.debug("get exdata for task vid:%s" % vid)

                    cracker = self._cracker[site]
                    log.app_log.debug("crack, url: %s, vid: %s" % (url, vid))
                    result = cracker.crack(dpara)

                    if result and result.get("error", -1) != 1 and result_key:
                        result["vid"] = vid
                        result["site"] = site
                        result["url"] = url
                        self._redis.set_data(result_key, json.dumps(result), ttl=self.get_ttl(site))
                    else:
                        self._redis.delete_data(extra_key)
                        if self._multi_redis:
                            self._multi_redis.delete_data(extra_key)
                        log.app_log.error("crack fail, vid: %s, task FAIL" % vid)
                else:
                    log.app_log.error("crack fail:no extra info for task vid: %s, task FAIL" % vid)
        except Exception, e:
            log.app_log.error("crack fail:task vid: %s, task FAIL" % vid)
            log.app_log.error(traceback.format_exc())

if __name__ == '__main__':
    n = 1
    wl = {}
    try:
        n = int(sys.argv[1])
        print "启动%s个worker" % n
    except Exception,e:
        n = 1
        print "启动%s个worker" % n
    for k in range(0,n):
        wl[k] = CrackWorker()

    for k in wl:
        wl[k].start()
    
    #for k in wl:
    #    wl[k].join()
    #try:
    #    pid = os.fork()
    #    if pid == 0:
    #        p = CrackWorker()
    #        p.run()
    #    else:
    #        print 'parent process'
    #except OSError,e:
    #    pass
    #    print e
    #p = CrackWorker()
    #p.start()
    #p.join()


