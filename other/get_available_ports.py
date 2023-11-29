import serial.tools.list_ports

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

if __name__ == "__main__":
    available_ports = get_available_ports()

    if available_ports:
        print("Available ports:")
        for port in available_ports:
            print(port)
    else:
        print("No ports available.")