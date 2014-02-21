#!/usr/bin/env python

import random

from connect import connect


def run():
    # use the connect example
    rpc = connect()

    # Get the handler named 'neopixel'
    handler = rpc.get_handler_by_name("neopixel")

    pixel_count = handler.getPixelCount()

    for i in range(1, pixel_count):
        handler.setPixelColor(
            i,
            (
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255)
            )
        )


if __name__ == "__main__":
    run()
