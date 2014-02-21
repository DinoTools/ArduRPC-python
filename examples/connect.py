#!/usr/bin/env python

import serial
import ardurpc


def connect():
    # Connect to the serial port
    #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    # Load all handlers
    ardurpc.load_handlers()

    # New instance
    rpc = ardurpc.ArduRPC(serial=ser)

    print('Version(Protocol): {0}'.format(rpc.getProtocolVersion()))
    print('Version(Library): {0}'.format('.'.join([str(i) for i in rpc.getLibraryVersion()])))
    print('Handlers: {0}'.format(', '.join(rpc.get_handler_names())))

    return rpc

if __name__ == "__main__":
    connect()
