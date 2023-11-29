import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    ports_description = [port.device + ": " + port.description for port in ports]
    return ports_description

available_ports = get_available_ports()
print(available_ports)

def on_select(event):
    selected_item = dropdown_var.get()
    print(f"Selected item: {selected_item}")

# Create the main window
root = tk.Tk()
root.title("Dropdown List Example")

# Create a StringVar to hold the selected item
dropdown_var = tk.StringVar()

# Create a dropdown list
options = get_available_ports()
dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=options, state="readonly")
dropdown.set("Select port")  # Set the default value
dropdown.bind("<<ComboboxSelected>>", on_select)  # Bind the event handler

# Pack the dropdown list
dropdown.pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
