#!/usr/bin/env python
"""
Basic example.

Connects to an Arduino using the ArduRPC protocol and displays some information.

Change the connect() function to reflect your settings.
"""

import ardurpc
from ardurpc.connector import Serial, UDP


def connect():
    # Connect to the serial port
    con = Serial("/dev/ttyACM0", 9600)

    # More examples:
    # con = Serial("/dev/ttyUSB0", 9600)
    # con = UDP(host="192.168.1.1", port=1234)

    # New instance
    rpc = ardurpc.ArduRPC(connector=con)

    print("Version(Protocol): {0}".format(rpc.getProtocolVersion()))
    print(
        "Version(Library): {0}".format(
            ".".join([str(i) for i in rpc.getLibraryVersion()])
        )
    )
    print(
        "Available handlers: {0}".format(
            ", ".join(rpc.get_handler_names())
        )
    )

    return rpc

if __name__ == "__main__":
    connect()
