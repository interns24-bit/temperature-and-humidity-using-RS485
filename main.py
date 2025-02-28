import minimalmodbus
import serial
import time
from influxdb import InfluxDBClient

# Initialize InfluxDB Connection
client = InfluxDBClient(host='localhost', port=8086, database='sensor_data')

# Define USB Port and Modbus ID
PORT = "/dev/ttyUSB0"
SLAVE_ID = 2  # Change if necessary

# Function to initialize the sensor connection
def connect_sensor():
    sensor = minimalmodbus.Instrument(PORT, SLAVE_ID)
    sensor.serial.baudrate = 9600
    sensor.serial.bytesize = 8
    sensor.serial.parity = serial.PARITY_NONE
    sensor.serial.stopbits = 1
    sensor.serial.timeout = 2  # Increased timeout for stability
    return sensor

# Initialize sensor
sensor = connect_sensor()

try:
    while True:
        try:
            # Read raw 16-bit values
            raw_humidity = sensor.read_register(0, 0, functioncode=3, signed=False)
            raw_temperature = sensor.read_register(1, 0, functioncode=3, signed=True)

            # Convert raw values (scale down by 10 as per datasheet)
            humidity = raw_humidity / 10.0
            temperature = raw_temperature / 10.0

            # Log Data to InfluxDB
            data = [
                {
                    "measurement": "sensor_readings",
                    "fields": {
                        "temperature": temperature,
                        "humidity": humidity
                    }
                }
            ]
            client.write_points(data)

            # Print results every 2 seconds
            print(f"🌡Temperature: {temperature:.1f}°C | 💧Humidity: {humidity:.1f}%RH")

        except minimalmodbus.NoResponseError:
            print("❌ No response from sensor! Reconnecting...")
            time.sleep(5)  # Wait before retrying
            sensor = connect_sensor()  # Reinitialize connection

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(5)

        time.sleep(2)  # Read every 2 seconds

except KeyboardInterrupt:
    print("❌›‘ Stopping system...")

