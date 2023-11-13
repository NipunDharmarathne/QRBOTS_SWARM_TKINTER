import tkinter as tk
import webbrowser

def open_map():
    location = location_var.get()
    if location == "Location 1":
        url = "https://www.google.com/maps/place/Location1"
    elif location == "Location 2":
        url = "https://www.google.com/maps/place/Location2"
    webbrowser.open(url)

root = tk.Tk()
root.geometry(f"{400}x{200}")
root.title("Map Selection")

location_var = tk.StringVar()
location_var.set("Select a Location")

label = tk.Label(root, text="Select a map location:")
label.pack(pady=10)

location_dropdown = tk.OptionMenu(root, location_var, "Location 1", "Location 2")
location_dropdown.pack()

show_map_button = tk.Button(root, text="Show Map", command=open_map)
show_map_button.pack(pady=10)

root.mainloop()
