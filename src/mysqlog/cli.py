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
    user: str = typer.Option(..., "-u", "--user"),
    password: str = typer.Option(..., "-p", "--password"),
    host: str = typer.Option("localhost", "-h", "--host"),
    database: str = typer.Option("test", "-d", "--database"),
):
    f = open(logpath)
    q = queue.Queue(100)

    producer = SlowQueryLogProducer(f, q)
    consumer = SlowQueryLogConsumer(q, host=host, user=user, password=password, database=database)

    producer.start()
    consumer.start()


if __name__ == "__main__":
    app()
