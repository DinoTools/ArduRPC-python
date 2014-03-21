"""
"""
import binascii
import time

import_error = None
try:
    import bluetooth
except ImportError as e:
    bluetooth = None
    import_error = e

from ardurpc.connector import BaseConnector
from ardurpc.exception import Timeout


class Bluetooth(BaseConnector):

    def __init__(self, address=None, **kwargs):
        if bluetooth == None:
            raise import_error
        BaseConnector.__init__(self, **kwargs)
        self.timeout = 3
        self.address = address
        self.socket = None
        self.uuid = "00001101-0000-1000-8000-00805f9b34fb"

        if self.auto_connect is True:
            self.connect()

    def __del__(self):
        if self.socket is not None:
            self.socket.close()

    def _call(self, data):
        hex_data = binascii.hexlify(data)
        #print("exec", hex_data)
        i = 0
        while i < 3:
            #print("in", self.serial.timeout)
            try:
                self.socket.send(b':' + hex_data + b'\n')
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
        Reade data from bluetooth and wait for the result.

        :return: Parsed result

        """

        time_start = time.time()
        data = b""
        while True:
            try:
                tmp = self.socket.recv(32)
            except bluetooth.BluetoothError:
                tmp = None

            time_diff = time.time() - time_start
            # no new data
            if tmp is None or len(tmp) == 0:
                if time_diff > self.timeout:
                    raise Timeout()
                continue

            data = data + tmp
            if data.find(b"\n") < 0:
                continue

            tmp = data.split(b"\n")
            data = tmp.pop(-1)
            for line in tmp:
                #print("read:", line)
                if line[:1] != b':':
                    continue
                line = line.rstrip()
                return binascii.unhexlify(line[1:])


    def connect(self):
        service_matches = bluetooth.find_service(address=self.address, uuid=self.uuid)
        #print(service_matches, self.address, self.uuid)
        if len(service_matches) == 0:
            return False

        host = service_matches[0]["host"]
        port = service_matches[0]["port"]

        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((host, port))
        self.socket.settimeout(0.1)

    def is_connected(self):
        if self.socket is not None:
            return True
        return False
