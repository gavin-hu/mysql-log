import time
import threading

from mysqlog.parser import SlowQueryLog


class SlowQueryLogProducer(threading.Thread):
    def __init__(self, file, queue, **config):
        threading.Thread.__init__(self, name=file.name)
        self.parser = SlowQueryLog(file)
        self.queue = queue
        self.config = config

    def run(self):
        #
        while True:
            try:
                entry = self.parser.next()
                #
                if self.config["queryTime"] > entry["query_time"]:
                    continue
                #
                self.queue.put(entry)
            except StopIteration:
                print("No more log, just sleep 5 seconds")
                time.sleep(1)
