# -*-coding:utf-8 -*-
import logging
import logging.config

import sys
sys.path.append('.')

logging.config.fileConfig('monitor/logger.conf')

cracker_logger = logging.getLogger('cracker')
expires_logger = logging.getLogger('expires')
k_letv_logger = logging.getLogger('k_letv')
k_hunantv_logger = logging.getLogger('k_hunantv')
k_youku_logger = logging.getLogger('k_youku')
k_sohu_logger = logging.getLogger('k_sohu')
k_wasu_logger = logging.getLogger('k_wasu')
k_pptv_logger = logging.getLogger('k_pptv')
k_iqiyi_logger = logging.getLogger('k_iqiyi')
k_1905_logger = logging.getLogger('k_1905')
flvcd_logger = logging.getLogger('flvcd')
funtv_logger = logging.getLogger('funtv')

if __name__ == '__main__':
    pass
