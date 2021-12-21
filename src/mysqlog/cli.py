#!/usr/bin/env python3

import typer
import queue
#
from mysqlog.producer import SlowQueryLogProducer
from mysqlog.consumer import SlowQueryLogConsumer

#
app = typer.Typer()


@app.command()
def main(
    logpath: str,
    env: str = typer.Option("default", "-e", "--env"),
    user: str = typer.Option(..., "-u", "--user"),
    password: str = typer.Option(..., "-p", "--password"),
    host: str = typer.Option("localhost", "-h", "--host"),
    port: int = typer.Option(3306, "-P", "--port"),
    database: str = typer.Option("test", "-d", "--database"),
    threadSize: int = typer.Option(1, "-t", "--thread-size"),
    since: str  = typer.Option(None, "-s", "--since"),
):
    #
    f = open(logpath)
    q = queue.Queue(100)
    #
    producer = SlowQueryLogProducer(f, q)
    producer.start()
    #
    for i in range(threadSize):
        name = "SlowQueryLogConsumer" + str(i)
        #
        consumer = SlowQueryLogConsumer(
            q, name=name, env=env, host=host, port=port, user=user, password=password, database=database, since=since
        )
        #
        consumer.start()

if __name__ == "__main__":
    app()
