import ardurpc
from ardurpc.handler import Handler


class Temperature(Handler):

    """Read values from a temperature sensor."""

    def __init__(self, **kwargs):
        Handler.__init__(self, **kwargs)

    def getMinValue(self):
        """
        Get the value of the lowest possible temperature/humidity measured by
        the sensor.

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x11)

    def getMaxValue(self):
        """
        Get the value of the highest possible temperature/humidity measured by
        the sensor.

        :return: Highest temperature
        :rtype: Float

        """
        return self._exec(0x12)

    def getAccuracy(self):
        """
        Get the accuracy of the measured value.

        :return: Accuracy
        :rtype: Float

        """
        return self._exec(0x13)

    def getValue(self):
        """
        Get the current value.

        :return: Temperature/Humidity
        :rtype: Float

        """
        return self._exec(0x14)

ardurpc.register(0x0401, Temperature)


class Humidity(Temperature):

    """Read values from a humidity sensor."""

    def __init__(self, **kwargs):
        Temperature.__init__(self, **kwargs)

ardurpc.register(0x0402, Humidity)


class TemperatureHumidity(Handler):

    """Read values from a temperature-humidity sensor."""

    def __init__(self, **kwargs):
        Handler.__init__(self, **kwargs)

    def getMinTemperatureValue(self):
        """
        Get the value of the lowest possible temperature measured by the sensor.

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x11)

    def getMaxTemperatureValue(self):
        """

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x12)

    def getTemperatureAccuracy(self):
        """

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x13)

    def getTemperature(self):
        """

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x14)

    def getMinHumidityValue(self):
        """
        Get the value of the lowest possible humidity measured by the sensor.

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x21)

    def getMaxHumidityValue(self):
        """

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x22)

    def getHumidityAccuracy(self):
        """

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x23)

    def getHumidity(self):
        """

        :return: Lowest temperature
        :rtype: Float

        """
        return self._exec(0x24)

ardurpc.register(0x0403, TemperatureHumidity)
