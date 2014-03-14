import ardurpc
from ardurpc.handler import Handler


class Base(Handler):
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

class Extended(Base):
    """Handler for the Extended Matrix type"""

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

    def drawFastVLine(self, x, y, h, color):
        color = self._prepare_color(color)
        return self._exec(0x21, '>hhhBBB', x, y, h, color[0], color[1], color[2])

    def drawFastHLine(self, x, y, w, color):
        color = self._prepare_color(color)
        return self._exec(0x22, '>hhhBBB', x, y, w, color[0], color[1], color[2])

    def drawRect(self, x, y, w, h, color):
        color = self._prepare_color(color)
        return self._exec(0x23, '>hhhhBBB', x, y, w, h, color[0], color[1], color[2])

    def fillRect(self, x, y, w, h, color):
        color = self._prepare_color(color)
        return self._exec(0x24, '>hhhhBBB', x, y, w, h, color[0], color[1], color[2])

    def invertDisplay(self, i):
        # ToDo:
        color = self._prepare_color(color)
        return self._exec(0x26, '>hhhhBBB', x, y, w, h, color[0], color[1], color[2])

    def drawCircle(self, x, y, radius, color):
        color = self._prepare_color(color)
        return self._exec(0x30, '>hhhBBB', x, y, radius, color[0], color[1], color[2])

    def fillCircle(self, x, y, radius, color):
        color = self._prepare_color(color)
        return self._exec(0x31, '>hhhBBB', x, y, radius, color[0], color[1], color[2])

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):
        color = self._prepare_color(color)
        return self._exec(0x32, '>hhhhhhBBB', x0, y0, x1, y1, x2, y2, color[0], color[1], color[2])

    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color):
        color = self._prepare_color(color)
        return self._exec(0x33, '>hhhhhhBBB', x0, y0, x1, y1, x2, y2, color[0], color[1], color[2])

    def drawRoundRect(self, x, y, w, h, radius, color):
        color = self._prepare_color(color)
        return self._exec(0x34, '>hhhhhBBB', x, y, w, h, radius, color[0], color[1], color[2])

    def fillRoundRect(self, x, y, w, h, radius, color):
        color = self._prepare_color(color)
        return self._exec(0x35, '>hhhhhBBB', x, y, w, h, radius, color[0], color[1], color[2])

    def drawChar(self, x, y, c, color, bg, size):
        c = c.encode('ASCII')
        color = self._prepare_color(color)
        bg = self._prepare_color(bg)
        return self._exec(0x40, '>hhBBBBBBBB', x, y, c[0], color[0], color[1], color[2], bg[0], bg[1], bg[2], size)

    def setCursor(self, x, y):
        return self._exec(0x41, '>hh', x, y)

    def setTextColor(self, color, bg=None):
        color = self._prepare_color(color)
        if bg is None:
            return self._exec(0x42, '>BBB', color[0], color[1], color[2])
        bg = self._prepare_color(bg)
        return self._exec(0x43, '>BBBBBB', color[0], color[1], color[2], bg[0], bg[1], bg[2])

    def setTextSize(self, size):
        return self._exec(0x44, '>B', size)

    def setTextWrap(self, wrap):
        if type(wrap) == bool:
            if wrap:
                wrap = 1
            else:
                wrap = 0
        return self._exec(0x45, '>B', wrap)

    def write(self, s):
        for c in s:
            c = c.encode('ASCII')
            res = self._exec(0x46, '>B', c[0])
            if res != 0:
                return res
        return 0

    def setRotation(self, rotation):
        return self._exec(0x50, '>B', rotation)

    def swapBuffers(self, copy=True):
        if type(copy) == bool:
            if copy:
                copy = 1
            else:
                copy = 0
        return self._exec(0x51, '>B', copy)

    def setAutoSwapBuffers(self, auto_swap=True):
        if type(auto_swap) == bool:
            if auto_swap:
                auto_swap = 1
            else:
                auto_swap = 0
        return self._exec(0x52, '>B', auto_swap)

    def drawBitmap(self, x, y, width, height, bitmap):
        bitmap_fmt = 'B' * 3 * width * height
        return self._exec(0x60, '>hhBBB' + bitmap_fmt, x, y, width, height, 2, *bitmap)

ardurpc.register(0x0200, Base, mask=8)
ardurpc.register(0x0280, Extended, mask=9)
