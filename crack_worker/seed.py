# -*-coding:utf-8 -*-
import cs
from redis_mgr import RedisMgr


class Seed(object):
    def __init__(self):
        self._redis = RedisMgr(cs.redis_ip, cs.redis_port, cs.redis_pwd)

    def get_iqiyi_seed(self):
        return "6ab6d0280511493ba85594779759d4ed"

    def get_youku_seed(self):
        return ""

    def set_iqiyi_seed(self):
        iseed = self.get_iqiyi_seed()
        ikey = cs.iqiyi_salt_key
        self._redis.set_data(ikey, iseed)

    def set_youku_seed(self):
        youku_key = "youku:ep:key"
        youku_data = "9e3633aadde6bfec"
        self._redis.set_data(youku_key, youku_data)

if __name__ == '__main__':
    seed = Seed()
    seed.set_iqiyi_seed()
    seed.set_youku_seed()

