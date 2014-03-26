"""
"""
import binascii
import socket
import time


from ardurpc.connector import BaseConnector
from ardurpc.exception import Timeout


class UDP(BaseConnector):

    def __init__(self, host, port=1234, **kwargs):
        BaseConnector.__init__(self, **kwargs)
        self.timeout = 3
        self.host = host
        self.port = port
        self.socket = None

        if self.auto_connect is True:
            self.connect()

    def __del__(self):
        if self.socket is not None:
            self.socket.close()

    def _call(self, data):
        i = 0
        while i < 3:
            try:
                print(data)
                self.socket.sendto(data, (self.host, self.port))
                result = self._get_result()
                return result
            except Timeout:
                pass

            time.sleep(1)
            i = i + 1

    def _get_result(self):
        """
        Wait for an incoming packet and return the data.

        :return: The result

        """

        time_start = time.time()
        data = b""
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                return data
            except socket.timeout:
                data = None

            time_diff = time.time() - time_start
            if time_diff > self.timeout:
                raise Timeout()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0.1)

    def is_connected(self):
        if self.socket is not None:
            return True
        return False
