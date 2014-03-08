import time

from ardurpc.exception import *


class Handler(object):

    """Handler base class."""

    def __init__(self, connector=None, handler_id=None, name=None):
        self.handler_id = handler_id
        self.name = name
        self.connector = connector
        self.timeout = 1

    def _exec(self, command_id, fmt=None, *data):
        """
        Execute a command on the microcontroller.

        :param Integer command_id: The ID of the command
        :param String fmt: The format of the data
        :param *data: Parameters for the command

        :return: Returns the result

        """

        return self.connector.exec(self.handler_id, command_id, fmt, *data)
