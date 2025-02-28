import minimalmodbus

PORT = "/dev/ttyUSB0"
for slave_id in range(1, 248):
    try:
        sensor = minimalmodbus.Instrument(PORT, slave_id)
        sensor.serial.baudrate = 9600
        sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
        sensor.serial.stopbits = 1
        sensor.serial.timeout = 1
        value = sensor.read_register(0, 0, functioncode=3)
        print(f"✅ Device found at ID {slave_id}, Value: {value}")
        break  # Stop after finding a device
    except:
        pass
