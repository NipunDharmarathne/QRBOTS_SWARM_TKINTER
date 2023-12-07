import serial.tools.list_ports
import serial.tools.list_ports_event

def port_changed(event):
    print("Port change detected!")
    print("Available ports:", get_available_ports())

if __name__ == "__main__":
    initial_ports = get_available_ports()
    print("Initial available ports:", initial_ports)

    event_listener = serial.tools.list_ports_event.Listener()
    event_listener.on_connect = port_changed
    event_listener.on_disconnect = port_changed
    event_listener.start()

    try:
        input("Press Enter to exit...\n")
    finally:
        event_listener.stop()
        event_listener.close()
