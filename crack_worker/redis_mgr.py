# -*-coding:utf-8 -*-
import traceback
from tornado import log
import redis

class RedisMgr(object):
    def __init__(self, host, port, passwd):
        self.host = host
        self.port = port
        self.passwd = passwd
        self._redis = redis.Redis(host=host, port=port, db=0, password=passwd)

    def check_connected(self):
        res = False
        try:
            cnt = 1
            while cnt < 50:
                if self._redis.ping():
                    res = True
                    break
                else:
                    cnt += cnt
                    self._redis = redis.Redis(host=self.host, port=self.port, db=0, password=self.passwd)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
        return res

    def set_data(self, key, data, ttl=None):
        try:
            if self.check_connected() and key and data:
                if ttl:
                    self._redis.set(key, data)
                    self._redis.expire(key, ttl)
                else:
                    self._redis.set(key, data)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
    
    def get_data(self, key):
        data = None
        try:
            if self.check_connected() and key:
                data = self._redis.get(key)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
        finally:
            return data
    
    def delete_data(self, key):
        try:
            if self.check_connected() and key:
                self._redis.delete(key)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
            
    def push_data(self, queue, data):
        try:
            if self.check_connected() and data:
                self._redis.rpush(queue, data)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def pop_data(self, queue):
        data = None
        try:
            if self.check_connected():
                data = self._redis.lpop(queue)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
        finally:
            return data 

class MultiRedisMgr(object):
    def __init__(self, redis_node):
        self._slaves = []
        self._masters = []
        for node in redis_node:
            for slave in node.get('slave', []):
                if slave.pop('local', None):
                    
                    self._slaves.append(RedisMgr(slave['host'], slave['port'], slave['passwd']))
            master = node.get('master', {})
            if not master.pop('local', None):
                self._masters.append(RedisMgr(*master))

    # 从本机slave读额外信息
    def get_data(self, key):
        data = None
        for r in self._slaves:
            data = r.get_data(key)
            if data:
                break
        return data

    # 删除其它master的额外信息
    def delete_data(self, key):
        for r in self._masters:
            r.delete_data(key)


if __name__ == "__main__":
    '''
    redis_mgr = RedisMgr('127.0.0.1', 6379, '')
    redis_mgr.set_data("test:key:1", 'k1')
    redis_mgr.set_data("test:key:2", 'k2')
    redis_mgr.push_data("test:list", 'q1')
    redis_mgr.push_data("test:list", 'q2')
    print redis_mgr.get_data("test:key:1")
    print redis_mgr.pop_data("test:list")
    redis_mgr.delete_data('test:key:1')
    print redis_mgr.get_data("test:key:1")
    '''
    r = RedisMgr('127.0.0.1', 7000, '')
    mr = MultiRedisMgr([('127.0.0.1', 7001, '')])
    r.set_data("test:key:1", 'k1')
    print mr.get_data("test:key:1")
