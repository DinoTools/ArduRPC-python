"""
ArduRPC exceptions.

* Failure

  * FunctionNotFound
  * HandlerNotFound
  * CommandNotFound

* Timeout

"""


class ArduRPCException(Exception):

    """Base ArduRPC Exception."""

    def __init__(self, value=""):
        Exception.__init__(self)

        self.value = value

    def __str__(self):
        return repr(self.value)


class Failure(ArduRPCException):

    """
    Something went wrong while executing a command.

    But no reason was given.

    """

    pass


class FunctionNotFound(Failure):

    """The function is not available on the microcontroller."""

    pass


class HandlerNotFound(Failure):

    """The handler is not available on the microcontroller."""

    pass


class InvalidHeader(Failure):

    """The header was malformed"""

    pass


class InvalidRequest(Failure):

    """The request was malformed"""

    pass


class CommandNotFound(Failure):

    """The command is not available on the microcontroller."""

    pass


class UnknownReturnCode(Failure):

    """."""

    pass


class Timeout(ArduRPCException):

    """A timeout occurred."""

    pass
