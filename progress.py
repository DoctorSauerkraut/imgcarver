import sys
import time
import threading

class Progress(threading.Thread):
    """
    Progress bar management thread
    """

    chronoStart = 0
    chronoEnd = 0
    bar_len = 60
    task = ""
    count = 0
    total = 0
    isrunning = True
    suffix = ''

    def __init__(self, task):
        threading.Thread.__init__(self)
        self.chronoStart = 0
        self.chronoEnd = 0
        self.task = task
        self.count = 0
        self.total = 0
        self.isrunning = True
        self.start()

    def run(self):
        while(self.isrunning is True):
            while(self.count != self.total or self.total != 0):
                filled_len = int(round(self.bar_len * self.count / float(self.total)))

                percents = round(100.0 * self.count / float(self.total), 1)
                bar = '#' * filled_len + '-' * (self.bar_len - filled_len)

                if(self.chronoStart != 0 and self.chronoEnd != 0):
                    delta = int((self.chronoEnd - self.chronoStart)/10000000)/100
                    self.chronoEnd = 0
                    self.chronoStart = 0
                    sys.stdout.write(str(self.task)+":\t"+'[%s] %s%s ...%s Done in %s secs\n' % (bar, percents, '%', self.suffix, delta))
                    self.isrunning = False
                    break
                else:
                    sys.stdout.write(str(self.task)+":\t"+'[%s] %s%s ...%s\r' % (bar, percents, '%', self.suffix))
                    sys.stdout.flush()
                time.sleep(0.1)

    def progress(self, count, total, suffix=''):
        if(count == 0):
            self.chronoStart = time.time_ns()
            self.chronoEnd = 0
            
        if(count == total):
            self.chronoEnd = time.time_ns()
        
        self.count = count
        self.total = total
        self.suffix = suffix