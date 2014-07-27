import ardurpc
from ardurpc.handler import Handler

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None


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
        return self._call(0x01)

    def getWidth(self):
        """
        Get the width in pixels.

        :return: Width
        :rtype: Integer

        """
        return self._call(0x02)

    def getHeight(self):
        """
        Get the height in pixels

        :return: Height
        :rtype: Integer

        """
        return self._call(0x03)

    def drawPixel(self, x, y, color):
        """
        Draw a pixel.

        :param Integer x: X-Position
        :param Integer y: Y-Position
        :param Integer|Tuple color: The color

        """
        color = self._prepare_color(color)
        return self._call(0x11, '>hhBBB', x, y, color[0], color[1], color[2])

    def drawLine(self, x0, y0, x1, y1, color):
        """
        Draw a line.

        """
        color = self._prepare_color(color)
        return self._call(0x21, '>hhhhBBB', x0, y0, x1, y1, color[0], color[1], color[2])

    def fillScreen(self, color):
        """
        Fill the screen with the given color.

        """
        color = self._prepare_color(color)
        return self._call(0x26, '>BBB', color[0], color[1], color[2])

class Extended(Base):
    """Handler for the Extended Matrix type"""

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

    def drawFastVLine(self, x, y, h, color):
        color = self._prepare_color(color)
        return self._call(0x22, '>hhhBBB', x, y, h, color[0], color[1], color[2])

    def drawFastHLine(self, x, y, w, color):
        color = self._prepare_color(color)
        return self._call(0x23, '>hhhBBB', x, y, w, color[0], color[1], color[2])

    def drawRect(self, x, y, w, h, color):
        color = self._prepare_color(color)
        return self._call(0x24, '>hhhhBBB', x, y, w, h, color[0], color[1], color[2])

    def fillRect(self, x, y, w, h, color):
        color = self._prepare_color(color)
        return self._call(0x25, '>hhhhBBB', x, y, w, h, color[0], color[1], color[2])

    def invertDisplay(self, i):
        # ToDo:
        color = self._prepare_color(color)
        return self._call(0x27, '>hhhhBBB', x, y, w, h, color[0], color[1], color[2])

    def drawCircle(self, x, y, radius, color):
        color = self._prepare_color(color)
        return self._call(0x31, '>hhhBBB', x, y, radius, color[0], color[1], color[2])

    def fillCircle(self, x, y, radius, color):
        color = self._prepare_color(color)
        return self._call(0x32, '>hhhBBB', x, y, radius, color[0], color[1], color[2])

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):
        color = self._prepare_color(color)
        return self._call(0x33, '>hhhhhhBBB', x0, y0, x1, y1, x2, y2, color[0], color[1], color[2])

    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color):
        color = self._prepare_color(color)
        return self._call(0x34, '>hhhhhhBBB', x0, y0, x1, y1, x2, y2, color[0], color[1], color[2])

    def drawRoundRect(self, x, y, w, h, radius, color):
        color = self._prepare_color(color)
        return self._call(0x35, '>hhhhhBBB', x, y, w, h, radius, color[0], color[1], color[2])

    def fillRoundRect(self, x, y, w, h, radius, color):
        color = self._prepare_color(color)
        return self._call(0x36, '>hhhhhBBB', x, y, w, h, radius, color[0], color[1], color[2])

    def drawChar(self, x, y, c, color, bg, size):
        c = c.encode('ASCII')
        color = self._prepare_color(color)
        bg = self._prepare_color(bg)
        return self._call(0x41, '>hhBBBBBBBB', x, y, c[0], color[0], color[1], color[2], bg[0], bg[1], bg[2], size)

    def setCursor(self, x, y):
        return self._call(0x42, '>hh', x, y)

    def setTextColor(self, color, bg=None):
        color = self._prepare_color(color)
        if bg is None:
            return self._call(0x43, '>BBB', color[0], color[1], color[2])
        bg = self._prepare_color(bg)
        return self._call(0x44, '>BBBBBB', color[0], color[1], color[2], bg[0], bg[1], bg[2])

    def setTextSize(self, size):
        return self._call(0x45, '>B', size)

    def setTextWrap(self, wrap):
        if type(wrap) == bool:
            if wrap:
                wrap = 1
            else:
                wrap = 0
        return self._call(0x46, '>B', wrap)

    def write(self, s):
        for c in s:
            c = c.encode('ASCII')
            res = self._call(0x47, '>B', c[0])
            if res != 0:
                return res
        return 0

    def setRotation(self, rotation):
        return self._call(0x51, '>B', rotation)

    def swapBuffers(self, copy=True):
        if type(copy) == bool:
            if copy:
                copy = 1
            else:
                copy = 0
        return self._call(0x52, '>B', copy)

    def setAutoSwapBuffers(self, auto_swap=True):
        if type(auto_swap) == bool:
            if auto_swap:
                auto_swap = 1
            else:
                auto_swap = 0
        return self._call(0x53, '>B', auto_swap)

    def drawImage(self, x, y, image, encoding=2):
        """
        """
        if encoding < 0 or encoding > 2:
            raise Exception("Encoding not supported")

        width = None
        height = None
        data = None
        if isinstance(image, (tuple, list)):
            width, height, data = image
        elif PILImage is not None and isinstance(image, PILImage.Image):
            width, height = image.size
            data = []
            for tmp_y in range(0, height):
                for tmp_x in range(0, width):
                    pixel = image.getpixel((tmp_x, tmp_y))
                    red, green, blue = pixel[:3]
                    color_data = None

                    if encoding == 0:
                        color_data = (int(red / 85) << 6) | (int(green / 36) << 3) | (int(blue / 36))
                        color_data = (color_data & 0xff, )
                    elif encoding == 1:
                        color_data = (int(red / 8) << 11) | (int(green / 4) << 5) | (int(blue / 8))
                        color_data = ((color_data >> 8), (color_data & 0xff))
                    elif encoding == 2:
                        color_data = (red, green, blue)

                    if color_data is None:
                        raise Exception("Something went wrong while encoding the image data")

                    data += color_data
        else:
            raise Exception("Image type not supported")

        return self._call(0x61, '>hhBBB%ds' % len(data), x, y, width, height, encoding, bytes(data))

ardurpc.register(0x0200, Base, mask=8)
ardurpc.register(0x0280, Extended, mask=9)
