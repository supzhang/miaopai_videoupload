#-*-coding:utf-8-*-
#用于线程调度
from PyQt5.QtCore import QThread,pyqtSignal
import time
class que(QThread):
    maxthreadSignal = pyqtSignal(int)

    def __init__(self,threads,maxthread):
        super().__init__()
        self.maxthread =maxthread
        self.threads = threads


    def run(self):

        while True:
            current_t = 0
            for tt in self.threads:
                if not tt[0].isFinished():  #检测是否完成
                    print('正在运行的线程1：', current_t)
                    if current_t < self.maxthread:  #检测是否最大线程
                        if not tt[0].isRunning():  #检测是否在运行
                           # print('启动',tt[1],'current',current_t,'maxthread',self.maxthread)
                            current_t += 1
                            tt[0].start()
                            current_t += 1
                            continue

                else:
                    tt[0].terminate()
                    tt[0].exit()
                    self.threads.remove(tt)
            #不关闭线程调度，一直等待新的线程进入。
            time.sleep(3)
            print('调度器等待——————————————————————')
            print('线程总数',len(self.threads))
            print('正在运行的线程：', current_t)
        pass
