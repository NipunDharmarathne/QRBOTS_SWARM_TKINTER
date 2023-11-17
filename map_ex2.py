import tkinter
import os
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# path for the database to use
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "offline_tiles_nyc.db")

# create map widget and only use the tiles from the database, not the online server (use_database_only=True)
map_widget = TkinterMapView(root_tk, width=1000, height=700, corner_radius=0, use_database_only=True,
                            max_zoom=19, database_path=database_path)
map_widget.pack(fill="both", expand=True)

map_widget.set_position(7.25963, 80.59915)
map_widget.set_zoom(19)

current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
location_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "location.png")).resize((10, 15)))
marker_1 = map_widget.set_marker(7.25974, 80.59904, text="52.55, 13.4", icon=location_image)

root_tk.mainloop()