import ardurpc
from ardurpc.handler import Handler


class PixelStripBase(Handler):

    """Wrapper."""

    def __init__(self, **kwargs):
        Handler.__init__(self, **kwargs)

    def _prepare_color(self, color):
        if type(color) == int:
            return (color, color, color)

        if type(color) == tuple:
            color = list(color)

        if type(color) == list:
            while(len(color) < 3):
                color.append(0)
        return color

    def getColorCount(self):
        """
        Return the number of colors.

        :return: Number of colors 1, 2 or 3
        :rtype: Integer

        """

        return self._exec(0x01)

    def getPixelCount(self):
        """
        Return the number of pixels.

        :return: Number of pixels
        :rtype: Integer

        """

        return self._exec(0x02)

    def setPixelColor(self, n, color):
        """
        Set the color of a pixel.

        :param Integer n: The pixel index (0 - (16^2)-1)
        :param List|Integer color: The color
        :return: command result

        """

        color = self._prepare_color(color)

        return self._exec(0x11, '>HBBB', n, color[0], color[1], color[2])

    def setRangeColor(self, start, end, color):
        """
        Set the color of a pixel.

        :param Integer start: The pixel to start
        :param Integer end: The pixel to stop
        :param List|Integer color: The color
        :return: command result

        """

        color = self._prepare_color(color)

        return self._exec(0x12, '>HHBBB', start, end, color[0], color[1], color[2])


ardurpc.register(0x0100, PixelStripBase, mask=8)
