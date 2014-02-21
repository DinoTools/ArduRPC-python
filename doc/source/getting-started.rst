===============
Getting Started
===============

Initialize the library
----------------------

Load all included handlers to enable auto detection::

    >>> import ardurpc
    >>> ardurpc.load_handlers()


Setup a connection
------------------

First off all setup a serial connection::

    >>> import serial
    >>> ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

Use the serial connection and initialize ArduRPC::

    >>> rpc = ardurpc.ArduRPC(serial=ser)


Use the ArduRPC interface
-------------------------

Get the supported protocol version. This should be 0::

    >>> rpc.getProtocolVersion()

Get the version of the ArduRPC library on the device. This should be a tuple with three elements::

    >>> rpc.getLibraryVersion()

Get a list of all handler names available on the device::

    >>> rpc.get_handler_names()

Get a handler named 'neopixel'::

    >>> handler = rpc.get_handler_by_name("neopixel")

Get the number of available pixels of the NeoPixel strip::

    >>> handler.getPixelCount()
