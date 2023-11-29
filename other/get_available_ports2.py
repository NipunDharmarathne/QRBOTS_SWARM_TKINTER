import serial.tools.list_ports

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    ports_description = [port.description for port in ports]
    return ports_description

available_ports = get_available_ports()
print(available_ports)
