import serial.tools.list_ports

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return ports

if __name__ == "__main__":
    available_ports = get_available_ports()

    if available_ports:
        print("Available ports:")
        for port in available_ports:
            print(f"Port: {port.device}")
            print(f"  Description: {port.description}")
            print(f"  Manufacturer: {port.manufacturer}")
            print(f"  HWID: {port.hwid}")
            print(f"  Serial Number: {port.serial_number}")
            print(f"  Location: {port.location}")
            print(f"  Product: {port.product}")
            print(f"  VID: {port.vid}")
            print(f"  PID: {port.pid}")
            print(f"  Interface: {port.interface}")
            print("\n" + "-"*30)
    else:
        print("No ports available.")
