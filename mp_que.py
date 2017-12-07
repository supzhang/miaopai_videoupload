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
                if not tt[0].isFinished():
                    current_t += 1
                    if current_t <= self.maxthread:
                        tt[0].start()

                else:
                    tt[0].terminate()
                    tt[0].exit()
                    #print('-------',tt)
                    self.threads.remove(tt)
            if current_t == 0:
                self.exit()
            time.sleep(3)
                    


        pass
