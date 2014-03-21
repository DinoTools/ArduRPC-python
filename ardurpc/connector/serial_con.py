"""
The serial connector.

It uses pySerial to open and manage connections to a ArduRPC device over a serial connection.
"""
# Only needed for Python <= 2.5 ?
#from __future__ import absolute_import

import binascii
import time

import serial

from ardurpc.connector import BaseConnector
from ardurpc.exception import Timeout


class Serial(BaseConnector):

    def __init__(self, port=None, baudrate=9600, **kwargs):
        BaseConnector.__init__(self, **kwargs)
        self.timeout = 3
        self.serial = None
        self.port = port
        self.baudrate = baudrate

        if self.auto_connect is True:
            self.connect()

    def _call(self, data):
        hex_data = binascii.hexlify(data)
        #print("exec", hex_data)
        i = 0
        while i < 3:
            #print("in", self.serial.timeout)
            try:
                self.serial.write(b':' + hex_data + b'\n')
                #print("out")
                result = self._get_result()
                #print("foo", result)
                return result
            except Timeout:
                #print("timeout")
                pass

            time.sleep(1)
            i = i + 1

    def _get_result(self):
        """
        Reade data from serial port and wait for the result.

        :return: Parsed result

        """

        time_start = time.time()
        while True:
            data = self.serial.readline()
            time_diff = time.time() - time_start
            if len(data) == 0:
                if time_diff > self.timeout:
                    raise Timeout()
                continue

            #print("read:", data)
            if data[:1] == b':':
                data = data.rstrip()
                #print(data)
                return binascii.unhexlify(data[1:])

            if time_diff > self.timeout:
                raise Timeout()

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)

    def is_connected(self):
        if self.serial is not None:
            return True
        return False
