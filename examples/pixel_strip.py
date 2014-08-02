#!/usr/bin/env python
"""
Control a pixel strip

This example uses the connect() function from the Basic example.
"""


from basic import connect


def run():
    # use the basic example
    rpc = connect()

    # Get a handler named 'strip'
    handler = rpc.get_handler_by_name("strip")
    if handler is None:
        print("A handler with the given name does not exist")

    # Get pixel count
    pixel_count = handler.getPixelCount()
    print("Strip has {0} pixels".format(pixel_count))

    # Set color to red
    for i in range(0, pixel_count):
        handler.setPixelColor(i, (255, 0, 0))

    # Set color to green
    for i in range(0, pixel_count):
        handler.setPixelColor(i, (0, 255, 0))

    # Set color to blue
    for i in range(0, pixel_count):
        handler.setPixelColor(i, (0, 0, 255))


if __name__ == "__main__":
    run()
