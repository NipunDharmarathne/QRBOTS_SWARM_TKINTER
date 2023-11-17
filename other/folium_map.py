import tkinter as tk
from tkinter import ttk
from folium import Map, Marker, Popup
from folium.plugins import MiniMap
from io import BytesIO
from PIL import Image, ImageTk

class FoliumMap(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.map = None

        self.initialize()

    def initialize(self):
        # Create a map using Folium
        self.map = Map(location=[37.7749, -122.4194], zoom_start=12)

        # Add a marker with a popup
        marker = Marker(location=[37.7749, -122.4194], popup=Popup("Hello, Folium!"))
        marker.add_to(self.map)

        # Add a MiniMap to the map
        minimap = MiniMap()
        minimap.add_to(self.map)

        # Convert Folium map to a PNG image
        map_png = self.get_map_image()

        # Create a Tkinter PhotoImage from the PNG image
        self.map_image = ImageTk.PhotoImage(map_png)

        # Create a label to display the map
        map_label = ttk.Label(self, image=self.map_image)
        map_label.grid(row=0, column=0, sticky="nsew")

        # Configure row and column weights to make the map label expand with the window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def get_map_image(self):
        # Convert Folium map to a PNG image
        map_data = self.map._to_png()
        map_image = Image.open(BytesIO(map_data))
        return map_image

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tkinter Folium Map Example")

    folium_map = FoliumMap(root)
    folium_map.pack(fill="both", expand=True)

    # Run the Tkinter event loop
    root.mainloop()
