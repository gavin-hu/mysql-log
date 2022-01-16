import time
import threading
import subprocess

from datetime import datetime
from shutil import which

from mysqlog.parser import SlowQueryLog


PT_FINGERPRINT_EXISTS = which("pt-fingerprint")


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
                if self.config["since"] and entry["datetime"] < datetime.strptime(
                    self.config["since"], "%Y-%m-%d %H:%M:%S"
                ):
                    print("filter by since: " + str(entry))
                    continue
                #
                if self.config["queryTime"] > entry["query_time"]:
                    print("filter by query_time: " + str(entry))
                    continue
                #
                if self.config["fingerprint"] and PT_FINGERPRINT_EXISTS:
                    entry["fingerprint"] = self.get_fingerprint(entry["query"])
                #
                self.queue.put(entry)
            except StopIteration:
                print("No more log, just sleep 5 seconds")
                time.sleep(1)

    def get_fingerprint(self, query):
        #
        output = subprocess.run(
            ["pt-fingerprint", "--query", query],
            stdout=subprocess.PIPE,
        )
        #
        if output.stdout:
            return output.stdout.decode("utf-8").strip()
        else:
            return None
