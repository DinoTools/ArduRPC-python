import ardurpc
from ardurpc.handler import Handler


class Base(Handler):
    """Handler for the Base Text-LCD type"""

    def __init__(self, **kwargs):
        Handler.__init__(self, **kwargs)

    def getWidth(self):
        """
        Get the display width as number of characters.

        :return: Width
        :rtype: Integer

        """
        return self._call(0x01)

    def getHeight(self):
        """
        Get the display height as number of characters.

        :return: Height
        :rtype: Integer

        """
        return self._call(0x02)

    def clear(self):
        """
        Clear the LCD screen and set the cursor position to the upper-left corner.
        """
        return self._call(0x11)

    def home(self):
        """
        Set the cursor position to the upper-left corner.
        """
        return self._call(0x12)

    def setCursor(self, col, row):
        """
        Position the cursor.

        """
        return self._call(0x13, '>BB', col, row)

    def write(self, c):
        """
        Print a single character to the LCD.

        """
        c = c.encode('ASCII')
        return self._call(0x21, '>B', c[0])

    def print(self, s):
        """
        Print text to the LCD.

        """
        s = s.encode('ASCII')
        return self._call(0x22, '>B%ds' % len(s), len(s), s)

ardurpc.register(0x0300, Base, mask=8)
