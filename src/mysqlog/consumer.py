import threading
import hashlib
import pymysql


class SlowQueryLogConsumer(threading.Thread):
    def __init__(self, queue, **config):
        threading.Thread.__init__(self, name="consumber")
        print(config)
        self.queue = queue
        self.connection = pymysql.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            cursorclass=pymysql.cursors.DictCursor,
        )

    def run(self):
        #
        while True:
            with self.connection.cursor() as cursor:
                entry = self.queue.get()
                entry["md5"] = hashlib.md5(
                    f"{entry['datetime']}{entry['query']}{entry['query_time']}".encode("utf-8")
                ).hexdigest()
                #
                print(entry)
                #
                insert_sql = "INSERT IGNORE INTO `mysql_slow_query_log` (`md5`, `datetime`, `database`, `user`, `host`, `query`, `query_time`, `lock_time`, `rows_examined`, `rows_sent`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                #
                cursor.execute(
                    insert_sql,
                    (
                        entry["md5"],
                        entry["datetime"],
                        entry["database"],
                        entry["user"],
                        entry["host"],
                        entry["query"],
                        entry["query_time"],
                        entry["lock_time"],
                        entry["rows_examined"],
                        entry["rows_sent"],
                    ),
                )
                #
                self.connection.commit()
