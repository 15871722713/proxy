#coding:utf-8

from getproxy import checkproxy
from sql import executesql
import Queue
import sys
import requests
import os
import threading
import time

class Worker(threading.Thread):    # 处理工作请求
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue


    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)    # get task
                res = callable(*args, **kwds)
                self.resultQueue.put(res)    # put result
            except Queue.Empty:
                break

class WorkManager:    # 线程池管理,创建
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()    # 请求队列
        self.resultQueue = Queue.Queue()    # 输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)    # 创建工作线程
            self.workers.append(worker)    # 加入到线程队列


    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()    # 从池中取出一个线程处理请求
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)    # 重新加入线程池中
        print '*'*40+'All jobs were complete.'+'*'*40


    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))    # 向工作队列中加入请求

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)

def main():
    try:
        num_of_threads = int(sys.argv[1])
    except:
        num_of_threads = 600
    _st = time.time()
    wm = WorkManager(num_of_threads)
    print 'num_of_threads :',num_of_threads   
    url = 'https://www.pornhub.com/'
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8'
              }
    sql = 'select * from iplist'
    for x in executesql(sql):
    	text = 'http://'+x[1]+':'+x[2]
    	text2 = 'https://'+x[1]+':'+x[2]
    	proxies = {"http": text,"https":text2}
        wm.add_job(checkproxy, x,url,proxies,header)
    wm.start()
    wm.wait_for_complete()
    print '*'*30+'Complete time:',time.asctime( time.localtime(time.time()) ),'*'*30
    print '*'*40+'Time use:',time.time() - _st,'*'*40

if __name__ == '__main__':
    main()