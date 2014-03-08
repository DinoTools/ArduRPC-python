import ardurpc
from .temperature_humidity import Temperature, Humidity, TemperatureHumidity


ardurpc.register(0x0401, Temperature)
ardurpc.register(0x0402, Humidity)
ardurpc.register(0x0403, TemperatureHumidity)
