import hashlib
import pymysql
import threading


class SlowQueryLogConsumer(threading.Thread):
    def __init__(self, queue, **config):
        threading.Thread.__init__(self, name=config["name"])
        self.queue = queue
        self.config = config

    def run(self):
        #
        self.connection = pymysql.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            cursorclass=pymysql.cursors.DictCursor,
        )
        #
        while True:
            entry = self.queue.get()
            #
            with self.connection.cursor() as cursor:
                entry["md5"] = hashlib.md5(
                    f"{entry['datetime']}{entry['query']}{entry['query_time']}".encode("utf-8")
                ).hexdigest()
                #
                print(entry)
                #
                insert_sql = "INSERT IGNORE INTO `mysql_slow_query_log` (`md5`, `env`, `datetime`, `database`, `user`, `host`, `fingerprint`, `query`, `query_time`, `lock_time`, `rows_examined`, `rows_sent`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                #
                cursor.execute(
                    insert_sql,
                    (
                        entry["md5"],
                        self.config["env"],
                        entry["datetime"],
                        entry["database"],
                        entry["user"],
                        entry["host"],
                        entry.get("fingerprint"),
                        entry["query"],
                        entry["query_time"],
                        entry["lock_time"],
                        entry["rows_examined"],
                        entry["rows_sent"],
                    ),
                )
                #
                self.connection.commit()
