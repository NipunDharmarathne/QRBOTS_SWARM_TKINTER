import tkinter
import os
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
from math import asin, atan2, cos, degrees, radians, sin

def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)


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
location_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "location.png")).resize((5, 8)))
marker_1 = map_widget.set_marker(7.25974, 80.59904, text="52.55, 13.4", icon=location_image)





def add_marker_event(coords):
    print("Add marker:", coords)
    
    distance = 0.005
    bearing = 90
        
    lat1_1 = coords[0]
    lon1_1 = coords[1]
    lat2_1, lon2_1 = get_point_at_distance(lat1_1, lon1_1, distance, bearing)
    lat3_1, lon3_1 = get_point_at_distance(lat2_1, lon2_1, distance, bearing)

    new_marker1_1 = map_widget.set_marker(lat1_1, lon1_1, text="1", icon=location_image)
    new_marker2_1 = map_widget.set_marker(lat2_1, lon2_1, text="2", icon=location_image)
    new_marker3_1 = map_widget.set_marker(lat3_1, lon3_1, text="3", icon=location_image)

    lat1_2, lon1_2 = get_point_at_distance(lat1_1, lon1_1, distance, 0)

    new_marker1_2 = map_widget.set_marker(lat1_2, lon1_2, text="4", icon=location_image)


map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)

def left_click_event(coordinates_tuple):
    map_widget.delete_all_marker()
    
map_widget.add_left_click_map_command(left_click_event)

root_tk.mainloop()