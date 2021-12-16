import threading
import pymysql


class SlowQueryLogConsumer(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self, name='consumber')
        self.queue = queue

    def run(self):
        #
        while True:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='123456',
                                         database='test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection:
                with connection.cursor() as cursor:
                    entry = self.queue.get()
                    print(entry)
                    #
                    insert_sql = "INSERT INTO `mysql_slow_query_log` (`datetime`, `database`, `user`, `host`, `query`, `query_time`, `lock_time`, `rows_examined`, `rows_sent`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    #
                    cursor.execute(insert_sql, (entry['datetime'], entry['database'], entry['user'], entry['host'],
                                                entry['query'], entry['query_time'], entry['lock_time'], entry['rows_examined'], entry['rows_sent']))
                    #
                connection.commit()
