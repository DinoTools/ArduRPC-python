import ardurpc
from ardurpc.handler.matrix_base import MatrixBase

class MatrixExtended(MatrixBase):
    """Handler for the Extended Matrix type"""

    def __init__(self, **kwargs):
        MatrixBase.__init__(self, **kwargs)

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

    def drawBitmap(self, x, y, bitmap, w, h, color):
        color = self._prepare_color(color)
        #return self._exec(0x41, '>hhhBBB', x, y, radius, color[0], color[1], color[2])

ardurpc.register(0x0280, MatrixExtended, mask=9)
