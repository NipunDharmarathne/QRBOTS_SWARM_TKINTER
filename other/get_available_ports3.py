import serial.tools.list_ports
import time

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    ports_description = [port.device + ": " + port.description for port in ports]
    return ports_description

def detect_port_changes(previous_ports):
    while True:
        current_ports = get_available_ports()

        if current_ports != previous_ports:
            print("Port change detected!")
            print("Available ports:", current_ports)
            previous_ports = current_ports

        time.sleep(1)  # Adjust the sleep duration based on your needs

if __name__ == "__main__":
    initial_ports = get_available_ports()
    print("Initial available ports:", initial_ports)

    detect_port_changes(initial_ports)
