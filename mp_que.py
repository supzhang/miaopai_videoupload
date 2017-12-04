#-*-coding:utf-8-*-
#用于线程调度
from PyQt5.QtCore import QThread
import time
class que(QThread):
    def __init__(self,threads):
        super().__init__()
        self.thread_no =2
        self.threads = threads

    def run(self):
        while True:
            current_t = 0
            for tt in self.threads:
                if not tt.isFinished():
                    current_t += 1
                    if current_t <= self.thread_no:
                        tt.start()

                else:
                    tt.terminate()
                    self.threads.remove(tt)
            if current_t == 0:
                self.exit()
            time.sleep(3)
                    


        pass
