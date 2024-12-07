from hardware.factory import HardwareFactory

class SensorService:
    def __init__(self):
        self.factory = HardwareFactory()

    def get_pressure_sensor_data(self):
        sensor = self.factory.create_pressure_sensor()
        return sensor.read_value()

    def get_analog_input_sensor_data(self):
        sensor = self.factory.create_analog_input_sensor()
        return sensor.read_value()

    def get_battery_voltage_data(self):
        sensor = self.factory.create_analog_input_sensor()
        return sensor.single_read(3)

# You can add more methods to interact with other sensors or actuators as needed.
