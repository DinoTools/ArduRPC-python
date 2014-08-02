ArduRPC Python
==============

Python library to control microcontroller based boards by using the ArduRPC protocol.

You can find more information in the `documentation`_.


Install
-------

**Requirements:**

* Python 2.7 or Python >= 3.2

**Requirements (optional):**

* `pyserial`_ >= 2.7

**Install:**

Install the basic ArduRPC library.

.. code-block:: console

    $ pip install ardurpc


Example
-------

The `pyserial`_ library is required to run the following example.

.. code-block:: python

    import ardurpc
    from ardurpc.connector import Serial, UDP

    # Connect to the serial port
    con = Serial("/dev/ttyACM0", 9600)

    # More examples:
    # con = Serial("/dev/ttyUSB0", 9600)
    # con = UDP(host="192.168.1.1", port=1234)

    # New instance
    rpc = ardurpc.ArduRPC(connector=con)

    print("Version(Protocol): {0}".format(rpc.getProtocolVersion()))
    print(
        "Version(Library): {0}".format(
            ".".join([str(i) for i in rpc.getLibraryVersion()])
        )
    )
    print(
        "Available handlers: {0}".format(
            ", ".join(rpc.get_handler_names())
        )
    )


License
-------

Published under the LGPLv3+ (see LICENSE for more information)

.. _`documentation`: http://ardurpc-python.readthedocs.org/
.. _`pyserial`: https://pypi.python.org/pypi/pyserial
