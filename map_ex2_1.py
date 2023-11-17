import tkinter
import os
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk


class ZoomableCanvas(tkinter.Canvas):
    def __init__(self, master=None, **kwargs):
        tkinter.Canvas.__init__(self, master, **kwargs)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scale_factor = 1.0

    def _on_mousewheel(self, event):
        # Respond to mouse wheel event to zoom in/out
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale("all", event.x, event.y, factor, factor)
        self.scale_factor *= factor


# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# path for the database to use
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "offline_tiles_nyc.db")

# # create map widget and only use the tiles from the database, not the online server (use_database_only=True)
map_widget = TkinterMapView(root_tk, width=1000, height=700, corner_radius=0, use_database_only=True,
                             max_zoom=19, database_path=database_path)
# map_widget.pack(fill="both", expand=True)

# map_widget.set_position(7.25963, 80.59915)
# map_widget.set_zoom(19)



zoomable_canvas = ZoomableCanvas(root_tk, width=400, height=300, background="white")
zoomable_canvas.pack(fill=tkinter.BOTH, expand=True)
# zoomable_canvas.create_rectangle(50, 50, 150, 150, fill="blue")

zoomable_canvas.create_window(0, 0, anchor="nw", window=map_widget)

root_tk.mainloop()