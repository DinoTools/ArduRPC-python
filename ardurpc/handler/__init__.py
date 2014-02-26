import binascii
import struct
import time

from ardurpc.exception import *


class Handler(object):

    """Handler base class."""

    def __init__(self, serial=None, handler_id=None, name=None):
        self.handler_id = handler_id
        self.name = name
        self.serial = serial
        self._type_map = {
            0x01: 'b',
            0x02: 'B',
            0x03: 'h',
            0x04: 'H',
            0x05: 'i',
            0x06: 'I',
            0x07: 'q',
            0x08: 'Q',
            0x09: 'f'
        }
        self.timeout = 1

    def _exec(self, command_id, fmt=None, *data):
        """
        Execute a command on the microcontroller.

        :param Integer command_id: The ID of the command
        :param String fmt: The format of the data
        :param *data: Parameters for the command

        :return: Returns the result

        """

        pkt_data = b''
        if fmt is not None:
            pkt_data = struct.pack(fmt, *data)
        pkt_head = struct.pack(
            'BBBB',
            0,
            self.handler_id,
            command_id,
            len(pkt_data)
        )

        hex_data = binascii.hexlify(pkt_head + pkt_data)
        #print("exec", hex_data)
        i = 0
        while i < 3:
            #print("in", self.serial.timeout)
            try:
                self.serial.write(b':' + hex_data + b'\n')
                #print("out")
                result = self._get_result()
                return result
            except Timeout:
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
            if data[0] == 58:  # ASCII(58) = :
                data = data.decode('ASCII')
                data = data.rstrip()
                #print(data)
                return self._parse_result(binascii.unhexlify(data[1:]))

            if time_diff > self.timeout:
                raise Timeout()

    def _parse_result(self, data):
        """
        Parse the result data.

        :param String data: Data to parse.

        :return: Mixed-Type

        """

        return_code = data[0]

        if return_code == 127:
            raise Failure()
        if return_code == 126:
            raise CommandNotFound()
        if return_code == 125:
            raise HandlerNotFound()
        if return_code == 124:
            raise FunctionNotFound()
        if return_code > 0:
            raise UnknownReturnCode()

        return_type = data[1]
        if return_type == 0x00:
            return return_code

        data = data[2:]
        if return_type in self._type_map:
            fmt = '>' + self._type_map[return_type]
            return struct.unpack(fmt, data[:struct.calcsize(fmt)])[0]

        # Array
        if return_type == 0x10:
            return_subtype = data[0]
            length = struct.unpack('>B', data[1:2])[0]
            data = data[2:]
            if return_subtype not in self._type_map:
                # ToDo
                raise Exception
            fmt = '>' + self._type_map[return_subtype] * length
            return struct.unpack(fmt, data[:struct.calcsize(fmt)])

        # String
        if return_type == 0x11:
            length = struct.unpack('>B', data[:1])[0]
            data = data[1:]
            name = struct.unpack('>%ds' % length, data[:length])[0]
            name = name.decode('ASCII').replace('\0', '').strip()
            return name

        # Multicolumn array
        if return_type == 0x12:
            rows = []
            fmt = '>'
            num_cols = struct.unpack('>B', data[:1])[0]
            data = data[1:]
            while num_cols > 0:
                num_cols = num_cols - 1
                col_type = struct.unpack('>B', data[:1])[0]
                data = data[1:]
                if col_type in self._type_map:
                    fmt = fmt + self._type_map[col_type]

            num_rows = struct.unpack('>B', data[:1])[0]
            data = data[1:]
            chunk_size = struct.calcsize(fmt)
            #print(fmt)
            while num_rows > 0:
                num_rows = num_rows - 1
                #print(data, num_rows, len(data), chunk_size)
                if len(data) < chunk_size:
                    print('Error')
                    # ToDo: error
                    continue
                rows.append(struct.unpack(fmt, data[:chunk_size]))
                data = data[chunk_size:]

            return rows
