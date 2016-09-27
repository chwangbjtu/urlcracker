import sys
sys.path.append('.')
from tornado import options

class Conf(object):
    #options.define('server_port', type=int)    
    #options.define('db_host', type=str)
    #options.define('db_port', type=int)
    #options.define('db_name', type=str)
    #options.define('db_user', type=str)
    #options.define('db_password', type=str)
    #options.define('common_sleep_time', type=int)

    options.define('http_read_size', type=int)
    options.define('http_sleep_time', type=int)
    options.define('http_retry_times', type=int)
    
    options.define('cracker_monitor_sleep_time', type=int)
    options.define('expires_monitor_sleep_time', type=int)

    options.define('k_letv_expires_time', type=int)
    options.define('k_hunantv_expires_time', type=int)
    options.define('k_youku_expires_time', type=int)
    options.define('k_sohu_expires_time', type=int)
    options.define('k_wasu_expires_time', type=int)
    options.define('k_pptv_expires_time', type=int)
    options.define('k_iqiyi_expires_time', type=int)
    options.define('k_1905_expires_time', type=int)
    options.define('deviation', type=int)

    options.define('mail_server', type=str)
    options.define('mail_username', type=str)
    options.define('mail_password', type=str)
    options.define('mail_from', type=str)
    options.define('mail_to', type=str)
    options.define('mail_cc', type=str)

    options.parse_config_file('monitor/ps.conf')

    #server_port = options.options.server_port
    #db_host = options.options.db_host
    #db_port = options.options.db_port
    #db_name = options.options.db_name
    #db_user = options.options.db_user
    #db_password = options.options.db_password
    #common_sleep_time = options.options.common_sleep_time
    http_read_size = options.options.http_read_size
    http_sleep_time = options.options.http_sleep_time
    http_retry_times = options.options.http_retry_times

    cracker_monitor_sleep_time = options.options.cracker_monitor_sleep_time
    expires_monitor_sleep_time = options.options.expires_monitor_sleep_time

    k_letv_expires_time = options.options.k_letv_expires_time
    k_hunantv_expires_time = options.options.k_hunantv_expires_time
    k_youku_expires_time = options.options.k_youku_expires_time
    k_sohu_expires_time = options.options.k_sohu_expires_time
    k_wasu_expires_time = options.options.k_wasu_expires_time
    k_pptv_expires_time = options.options.k_pptv_expires_time
    k_iqiyi_expires_time = options.options.k_iqiyi_expires_time
    k_1905_expires_time = options.options.k_1905_expires_time
    deviation = options.options.deviation

    mail_server = options.options.mail_server
    mail_username = options.options.mail_username
    mail_password = options.options.mail_password
    mail_from = options.options.mail_from
    mail_to = options.options.mail_to
    mail_cc = options.options.mail_cc

if __name__ == "__main__":
    conf = Conf()
