from ghost import Ghost, Session
import traceback
import time
from tornado import log

class YoukuGhostDriver(object):

    def __init__(self, host, port, timeout):
        #url = 'http://111.161.35.198:12210/youku_ghost.html'
        url = 'http://%s:%s/youku_ghost.html' % (host, port)
        self.ghost = Ghost()
        self.session = Session(self.ghost, wait_timeout=timeout, plugins_enabled=True)
        self.session.open(url)

    def parse(self, vid):
        try:
            res = []
            self.session.evaluate('window.getPlayUrl("%s")' % vid)
            success, resources = self.session.wait_for_selector('div[id="ck"]')
            if success:
                ck = self.session.evaluate('document.getElementById("ck").innerHTML');
                res = ck[0]

        except Exception, e:
            log.app_log.error(traceback.format_exc())

        finally:
            return res

if __name__ == "__main__":

    driver = YoukuGhostDriver()
    res = driver.parse('XMTM0NTA5MTE5Mg==')
    #res = driver.parse('XMTI4MDEyMzEy')
    print res
