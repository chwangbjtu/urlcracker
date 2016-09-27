# -*- coding:utf-8 -*-
import time
import json
import hashlib
import traceback
from tornado import log

import smtplib
from email.header import Header
from email.mime.text import MIMEText

import sys
sys.path.append('.')
from monitor.conf import Conf
from monitor.http_client import HttpDownload
from logger import cracker_logger, expires_logger, k_letv_logger, k_hunantv_logger, k_youku_logger, k_sohu_logger, k_wasu_logger, k_pptv_logger, k_iqiyi_logger, k_1905_logger
from logger import flvcd_logger, funtv_logger

class Util(object):

    httpclient = HttpDownload()

    loggers = {
                    "cracker":cracker_logger, 'expires':expires_logger, 
                    "flvcd":flvcd_logger, "funtv":funtv_logger,
                    "letv":k_letv_logger, "hunantv":k_hunantv_logger, "youku":k_youku_logger, 
                    "sohu":k_sohu_logger, "wasu":k_wasu_logger, "pptv":k_pptv_logger,
                    "iqiyi":k_iqiyi_logger, "1905":k_1905_logger, 
                }
    
    #转换成可读大小
    def humanization(self, size, type='M'):
        try:
            if type.upper() == 'M':
                return size / (1024.0 * 1024.0)
            elif type.upper() == 'K':
                return size / 1024.0 
            else:
                return size
        except Exception as e:
            log.app_log.error(traceback.format_exc())
    
    #对data生成md5
    def create_md5(self, data):
        try:
            md5 = hashlib.md5()
            md5.update(data)
            return md5.hexdigest()
        except Exception as e:
            log.app_log.error(traceback.format_exc())
        
    #日志处理
    def handle_msg(self, handle_name, msg):
        try:
            msg['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S')
            msg_str = json.dumps(msg, ensure_ascii=False)
            #保存日志
            if handle_name in self.loggers:
                logger = self.loggers[handle_name]
                logger.info(msg_str)
            #发送邮件通知
            if msg['level'] == 'error':
                self.send_mail(msg) 
        except Exception as e:
            log.app_log.error(traceback.format_exc())
    
    #发送邮件
    def send_mail(self, msg):
        try:
            msg_str = json.dumps(msg, ensure_ascii=False)
            msg = MIMEText(msg_str, 'html', 'utf-8')
            msg['Subject'] = Header('破解程序状态监控报告', 'utf-8')
            msg['To'] = Conf.mail_to
            msg['From'] = Conf.mail_from
            smtp = smtplib.SMTP() 
            smtp.connect(Conf.mail_server)
            smtp.login(Conf.mail_username, Conf.mail_password)
            mail_to = Conf.mail_to.split(',')
            smtp.sendmail(Conf.mail_from, mail_to, msg.as_string())
            smtp.close()
        except Exception as e:
            log.app_log.error('发送邮件失败')
            log.app_log.error(traceback.format_exc())
    
    #解析破解的结果，返回破解地址
    def parse_cracker(self, result, site, format):
        res = {'error':0, 'url':''}
        try:
            if not result or 'error' in result:
                msg = {'from':'expires', 'code':'', 'descript':'破解结果为空或出现error', 'site':site, 'format':format, 'level':'debug'}
                self.handle_msg(site, msg)
                #虽正常，但无url
                res['error'] = ParseCrackerType.CrackerError
                return res
            if result['type'] == '0':
                seg = result['seg']
                if format not in seg:
                    msg = {'from':'expires', 'code':'', 'descript':'破解结果不包含给定的format', 'site':site, 'format':format, 'level':'debug'}
                    self.handle_msg(site, msg)
                    #虽正常，但无url
                    res['error'] = ParseCrackerType.FormatNotFound
                    return res
                url = seg[format][0]['url']
                res['error'] = ParseCrackerType.Success
                res['url'] = url 
                return res
            elif result['type'] == '1': 
                seg = result['seg']
                if format not in seg:
                    msg = {'from':'expires', 'code':'', 'descript':'破解结果不包含给定的format', 'site':site, 'format':format, 'level':'debug'}
                    self.handle_msg(site, msg)
                    #虽正常，但无url
                    res['error'] = ParseCrackerType.FormatNotFound
                    return res
                url = seg[format][0]['url']
                custom_result = self.parse_custom(url, site, format)
                if not custom_result:
                    res['error'] = ParseCrackerType.Fail
                    return res
                start = result['start']
                startIndex = custom_result.find(start)
                if startIndex < 0:
                    res['error'] = ParseCrackerType.Fail
                    return res
                startIndex = startIndex + len(start)
                custom_result = custom_result[startIndex:]
                end = result['end']
                endIndex = custom_result.find(end)
                if endIndex < 0:
                    res['error'] = ParseCrackerType.Fail
                    return res
                url = custom_result[:endIndex]
                url = url.replace('\\','')
                res['error'] = ParseCrackerType.Success
                res['url'] = url 
                return res
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            res['error'] = ParseCrackerType.Fail
        finally:
            return res
    
    #发送二次请求，解析二次请求的结果，返回破解地址
    def parse_custom(self, url, site, format):
        #对于网络获取不到数据，测试3遍后才得出结论
        count = 0
        while count < Conf.http_retry_times:
            try:
                http_result = self.httpclient.get_data(url) 
                if not http_result['data']:
                    msg = {'from':'expires', 'code':http_result['code'], 'descript':http_result['reason'], 'site':site, 'format':format, 'level':'debug'}
                    self.handle_msg(site, msg)
                    if count == Conf.http_retry_times - 1:
                        msg = {'from':'expires', 'code':'', 'descript':'连接3次无法从二次请求获取数据', 'site':site, 'format':format, 'level':'debug'}
                        self.handle_msg(site, msg)
                        return '' 
                else:
                    return http_result['data'] 
                sleep_time = Conf.http_sleep_time + count * 3; 
                time.sleep(sleep_time)
            except Exception, e:
                log.app_log.error(traceback.format_exc())
            finally:
                count = count + 1


class ParseCrackerType(object):
    #error: 0-正常， 1-出错  2-cracker出错  3-视频不包含给定format
    Success = 0
    Fail = 1
    CrackerError = 2
    FormatNotFound = 3

if __name__ == '__main__':
    util = Util()
    util.send_mail('test')
