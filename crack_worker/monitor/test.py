# -*- coding:utf-8 -*-
from multiprocessing import Process

import sys
sys.path.append('.')
from monitor.cracker_monitor import CrackerMonitor
from monitor.expires_monitor import ExpiresMonitor

if __name__ == '__main__':

    procs = []

    procs.append(CrackerMonitor())
    procs.append(ExpiresMonitor())

    for proc in procs:
        proc.start()

    for porc in procs:
        proc.join()
