import time
import threading
#
from mysqlog.parser import SlowQueryLog


class SlowQueryLogProducer(threading.Thread):

    def __init__(self, file, queue):
        threading.Thread.__init__(self, name=file.name)
        self.parser = SlowQueryLog(file)
        self.queue = queue

    def run(self):
        #
        while True:
            try:
                entry = self.parser.next()
                #
                self.queue.put(entry)
            except StopIteration:
                print('No more log, just sleep 5 seconds')
                time.sleep(1)
