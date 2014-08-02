import os

from ardurpc.handler import Handler

from ardurpc.__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)


_global_handlers = {}


class ArduRPC(Handler):

    """

    Functions with camel-case names are directly mapped to a function on the
    device. Functions without camel-case names are not mapped. The second
    function type should be preferred.

    """

    def __init__(self, handlers=None, **kwargs):
        Handler.__init__(self, **kwargs)
        self.handler_id = 255

        self._handlers = handlers

        self._handler_cache = []
        for (handler_id, handler_type) in self.getHandlerList():
            handler = None
            mask = 16
            while mask > 0 and handler is None:
                tmp_mask = (0xffff << (16 - mask)) & 0xffff
                tmp_handler_id = handler_type & tmp_mask
                if self._handlers is not None:
                    handler = self._handlers.get(tmp_handler_id, None)
                else:
                    handler = _global_handlers.get(tmp_handler_id, None)

                if handler is not None and handler.get("mask") != mask:
                    handler = None

                mask = mask - 1

            if handler is None:
                continue
            handler = handler.get("handler")
            name = self.getHandlerName(handler_id)
            self._handler_cache.append(handler(connector=self.connector, handler_id=handler_id, name=name))

    def getProtocolVersion(self):
        """
        Get supported protocol version.

        :return: Value returned by the device

        """

        return self._call(0x01)

    def getLibraryVersion(self):
        """
        Get the version of the ArduRPC library running on the device.

        :return: Raw value returned by the device

        """

        return self._call(0x02)

    def getMaxPacketSize(self):
        """
        Get the max packet size supported by the device.

        :return: Raw value returned by the device

        """

        return self._call(0x03)

    def getFunctionList(self):
        return self._call(0x10)

    def getHandlerList(self):
        """
        Get a handler list.

        Function 'get_handlers()' should be preferred.

        :return: Raw value returned by the device

        """

        return self._call(0x20)

    def getHandlerName(self, handler_id):
        """
        Get a handler name by its ID.

        :param Integer handler_id: The ID of the handler
        :return: The name of the handler
        :rtype: String

        """

        return self._call(0x21, '>B', handler_id)

    def get_handler(self, handler_id):
        """
        Return a instance of the handler.

        :param Integer handler_id: The ID of the handler
        :return: Class instance or None
        :rtype: Instance

        """

        for handler in self._handlers:
            if handler.handler_id == handler_id:
                return handler
        return None

    def get_handler_names(self):
        """
        Return a list of handler names present on the device.

        :return: List of names
        :rtype: List

        """

        names = []
        for h in self._handler_cache:
            names.append(h.name)
        return names

    def get_handler_by_name(self, name):
        """
        Return a instance of the handler.

        :param String name: The name of the handler
        :return: Class instance or None
        :rtype: Instance

        """

        for handler in self._handler_cache:
            if handler.name == name:
                return handler
        return None

    def get_handlers(self):
        """
        Get a list of all available handlers.

        :return: Dict: Key = Name, Value = Instance
        :rtype: Dict

        """

        return self._handlers

    def get_handler_cache(self):
        """
        Get a list of all cached handlers.

        :return: Dict: Key = Name, Value = Instance
        :rtype: Dict

        """

        return self._handler_cache

    def get_version(self):
        """
        Get the version of the ArduRPC library running on the device.

        :return: A Dict with major, minor and patch level
        :rtype: Dict

        """

        version = self.getVersion()
        return {
            'major': version[0],
            'minor': version[1],
            'patch': version[2]
        }


def register(handler_type, handler, mask=16):
    """
    Register a new handler.

    :param Integer handler_type: The ID of the handler type
    :param Class handler: The handler class (Not an instance)
    :param Integer mask: The mask to group handlers

    """

    tmp_mask = (0xffff << (16 - mask)) & 0xffff
    tmp_handler_type = handler_type & tmp_mask
    if tmp_handler_type != handler_type:
        # ToDo: error
        print("error")
        return
    if handler_type in _global_handlers:
        return

    _global_handlers[handler_type] = {
        "handler": handler,
        "mask": mask
    }


def load_handlers():
    """Load build-in handlers."""

    import ardurpc.handler
    path = ardurpc.handler.__path__[0]
    for filename in os.listdir(path):
        if filename == "__init__.py":
            continue

        pkg = None
        if os.path.isdir(os.path.join(path, filename)) and \
           os.path.exists(os.path.join(path, filename, "__init__.py")):
            pkg = filename

        if filename[-3:] == '.py':
            pkg = filename[:-3]

        if pkg is None:
            continue

        try:
            __import__("ardurpc.handler." + pkg, locals(), globals())
        except Exception as msg:
            print(str(msg))

load_handlers()
