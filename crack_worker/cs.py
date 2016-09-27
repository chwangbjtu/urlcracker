#/usr/bin/python
# -*- coding:utf-8 -*-
#[redis]
redis_ip = "192.168.16.158"
redis_port = 7000
redis_pwd  = ""
redis_node_on = True
redis_node = [
                {
                 'master': {'host': '192.168.28.210', 'port': 7000, 'passwd': '', 'local': True},
                 'slave':
                        [
                         {'host': '192.168.16.165', 'port': 7001, 'passwd': '', 'local': False},
                        ],
                },
                {
                 'master': {'host': '192.168.16.165', 'port': 7000, 'passwd': '', 'local': False},
                 'slave':
                        [
                         {'host': '192.168.28.210', 'port': 7001, 'passwd': '', 'local': True},
                        ],
                },
             ]

#[site_deadline]
ttl = '{"youku":"7200","sohu":"7200","iqiyi":"7200","hunantv":"7200","letv":"600","wasu":"7200","pptv":"7200", "1905":"7200"}'

#[extra_data_deadline]
edd_ttl = 604800    #7*24*60*60

#[log]
logging='DEBUG'
log_file_max_size = 100000000
log_file_prefix = 'log/ps.log'
log_file_num_backups=30

#[driver]
driver_type = 'app'
#ms为单位
youku_driver_timeout = 2000
qq_driver_timeout = 5000
#driver_type = 'phantomjs'

#[iqiyi]
iqiyi_type = 'h5'
#iqiyi_type = 'swf'
iqiyi_salt_key = 'iqiyi_salt_key'

#[worker]
worker_sleep_time = 0.5 # 500ms  

#[phantomjs]暂时不用
phantomjs_timeout = 1000 #该值需要随着phantomjs的进程数来调整

#[apache]
apache_host = '192.168.16.159'
apache_port = 80
