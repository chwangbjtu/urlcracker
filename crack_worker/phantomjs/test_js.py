import time
import commands
from multiprocessing import Process

def start():
    while True:
        now = time.time() 
        res = commands.getstatusoutput('phantomjs --load-plugins=true youku.js 1000 http://192.168.16.159/youku.html?id=XMTQxNDUxMzUyNA==')
        print time.time() - now
        print res

if __name__ == '__main__':
    procs = [] 
    for i in range(3):
        procs.append(Process(target = start))
    for proc in procs:
        proc.start()
    for porc in procs:
        proc.join()
