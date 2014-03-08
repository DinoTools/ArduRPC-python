import ardurpc
from ardurpc.handler.matrix import Extended


class Colorduino_GFX(Extended):
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
