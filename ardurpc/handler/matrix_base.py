import ardurpc
from ardurpc.handler import Handler


class MatrixBase(Handler):
    """Handler for the Base Matrix type"""

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
        Get the color count.

        :return: Number of colors
        :rtype: Integer

        """
        return self._exec(0x01)

    def getWidth(self):
        """
        Get the width in pixels.

        :return: Width
        :rtype: Integer

        """
        return self._exec(0x02)

    def getHeight(self):
        """
        Get the height in pixels

        :return: Height
        :rtype: Integer

        """
        return self._exec(0x03)

    def drawPixel(self, x, y, color):
        """
        Draw a pixel.

        :param Integer x: X-Position
        :param Integer y: Y-Position
        :param Integer|Tuple color: The color

        """
        color = self._prepare_color(color)
        return self._exec(0x11, '>hhBBB', x, y, color[0], color[1], color[2])

    def drawLine(self, x0, y0, x1, y1, color):
        """
        Draw a line.

        """
        color = self._prepare_color(color)
        return self._exec(0x20, '>hhhhBBB', x0, y0, x1, y1, color[0], color[1], color[2])

    def fillScreen(self, color):
        """
        Fill the screen with the given color.

        """
        color = self._prepare_color(color)
        return self._exec(0x25, '>BBB', color[0], color[1], color[2])

ardurpc.register(0x0200, MatrixBase, mask=8)
