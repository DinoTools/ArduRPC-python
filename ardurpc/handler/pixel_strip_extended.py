import ardurpc
from ardurpc.handler.pixel_strip_base import PixelStripBase


class PixelStripExtended(PixelStripBase):

    """Wrapper."""

    def __init__(self, **kwargs):
        PixelStripBase.__init__(self, **kwargs)

    def show(self):

        """
        Transmit the current values to the LEDs.
        """

        self._exec(0x05, None)

ardurpc.register(0x0180, PixelStripExtended, mask=9)
