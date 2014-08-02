import ardurpc
from ardurpc.handler import Handler


class Board(Handler):
    """Handler for the Board"""

    def __init__(self, **kwargs):
        Handler.__init__(self, **kwargs)

    def getAnalogInput(self, pin):
        """
        Get the value of an analog input pin.

        :param Integer pin: Pin number
        """

        return self._call(0x11, ">B", pin)

    def getDigitalInput(self, pin):
        """
        Get the value of an digital input pin.

        :param Integer pin: Pin number

        :rtype: Boolean
        :return: False or True
        """

        value = self._call(0x21, ">B", pin)
        if value:
            return True
        else:
            return False

    def setDigitalOutput(self, pin, value):
        """
        Set the value of a digital output pin.

        :param Integer pin: Pin number
        :param Integer value: The value (0, 1, False, True)
        """
        if value is True:
            value = 1
        else:
            value = 0

        return self._call(0x22, ">BB", pin, value)

    def setPWMOutput(self, pin, value):
        """
        Set the value of a PWM output pin.

        :param Integer pin: Pin number
        :param Integer value: The PWM value (0-255)
        """
        return self._call(0x31, ">BB", pin, value)

ardurpc.register(0x0501, Board, mask=16)
