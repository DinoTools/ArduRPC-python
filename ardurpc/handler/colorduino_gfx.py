import ardurpc
from ardurpc.handler.matrix_extended import MatrixExtended


class Colorduino_GFX(MatrixExtended):
    """Wrapper."""
    def swapBuffers(self, copy=True):
        if type(copy) == bool:
            if copy:
                copy = 1
            else:
                copy = 0
        return self._exec(0xA0, '>B', copy)

    def setAutoSwapBuffers(self, auto_swap=True):
        if type(auto_swap) == bool:
            if auto_swap:
                auto_swap = 1
            else:
                auto_swap = 0
        return self._exec(0xA1, '>B', auto_swap)

ardurpc.register(0x0281, Colorduino_GFX)
