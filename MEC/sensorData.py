class SensorData:
    """A sample SensorData class"""

    def __init__(self, moisture, rainfall, humidity, temperature, crop_yield):
        self.moisture = moisture
        self.rainfall = rainfall
        self.humidity = humidity
        self.temperature = temperature
        self.crop_yield = crop_yield

    @property
    def climate_data(self):
        return '{} {} {} {} {}'.format(self.moisture, self.rainfall, self.humidity, self.temperature, self. crop_yield)

    def __repr__(self):
        return "Sensor({},{},{}, {}, {})".format(self.moisture, self.rainfall, self.humidity, self.temperature, self. crop_yield)