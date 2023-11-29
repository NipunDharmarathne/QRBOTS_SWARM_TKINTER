import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_item = dropdown_var.get()
    print(f"Selected item: {selected_item}")

# Create the main window
root = tk.Tk()
root.title("Dropdown List Example")

# Create a StringVar to hold the selected item
dropdown_var = tk.StringVar()

# Create a dropdown list
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=options, state="readonly")
dropdown.set("Select an option")  # Set the default value
dropdown.bind("<<ComboboxSelected>>", on_select)  # Bind the event handler

# Pack the dropdown list
dropdown.pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
