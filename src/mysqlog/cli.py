#!/usr/bin/env python3

import typer
import queue

from mysqlog.producer import SlowQueryLogProducer
from mysqlog.consumer import SlowQueryLogConsumer

app = typer.Typer()


@app.command()
def main(
    logpath: str,
    env: str = typer.Option(
        "default", "-e", "--env", help="The environment of mysql log to collect"
    ),
    user: str = typer.Option(..., "-u", "--user", help="The user of database for collecting"),
    password: str = typer.Option(
        ..., "-p", "--password", help="The password of database for collecting"
    ),
    host: str = typer.Option(
        "localhost", "-h", "--host", help="The host of database for collecting mysql log"
    ),
    port: int = typer.Option(
        3306, "-P", "--port", help="The port of database for collecting mysql log"
    ),
    database: str = typer.Option(
        "test", "-d", "--database", help="The database for collecting mysql log"
    ),
    threadSize: int = typer.Option(
        1, "-t", "--thread-size", help="The thread size of SlowQueryLogConsumer"
    ),
    since: str = typer.Option(
        None, "-s", "--since", help="Filter mysql log by datatime yyyy-MM-dd HH:mm:ss"
    ),
    queryTime: float = typer.Option(
        0.3, "-T", "--query-time", help="Filter mysql log by query_time"
    ),
    fingerprint: bool = typer.Option(
        False, "--enable-fingerprint", help="Enable query sql fingerprint"
    ),
):
    #
    f = open(logpath)
    q = queue.Queue(100)
    #
    producer = SlowQueryLogProducer(
        f, q, since=since, queryTime=queryTime, fingerprint=fingerprint
    )
    producer.start()
    #
    for i in range(threadSize):
        name = "SlowQueryLogConsumer" + str(i)
        #
        consumer = SlowQueryLogConsumer(
            q,
            name=name,
            env=env,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
        #
        consumer.start()


if __name__ == "__main__":
    app()
