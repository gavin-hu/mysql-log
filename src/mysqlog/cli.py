#!/usr/bin/env python3

import typer
import queue
#
from mysqlog.producer import SlowQueryLogProducer
from mysqlog.consumer import SlowQueryLogConsumer


def main(file) -> None:
    f = open(file)
    q = queue.Queue(100)

    producer = SlowQueryLogProducer(f, q)
    consumer = SlowQueryLogConsumer(q)

    producer.start()
    consumer.start()


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":
    typer.run(main)
