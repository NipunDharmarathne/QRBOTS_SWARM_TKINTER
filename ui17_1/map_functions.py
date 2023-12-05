import math
from math import asin, atan2, cos, degrees, radians, sin
import os
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
from tkinter import filedialog
import zipfile
import json

def calculate_distance_and_bearing(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    angle = math.atan2(x2 - x1, y2 - y1)
    angle_degrees = math.degrees(angle)
    return distance, angle_degrees

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
    return (degrees(lat2), degrees(lon2))

def create_map_widget(frame):
    # path for the database to use
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # database_path = os.path.join(script_directory, "offline_tiles_openstreet.db")
    database_path = os.path.join(script_directory, "offline_tiles_google_qbits.db")

    # create map widget and only use the tiles from the database, not the online server (use_database_only=True)
    map_widget = TkinterMapView(frame, width=1000, height=700, corner_radius=0, use_database_only=False,
                                max_zoom=19, database_path=database_path)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) 
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(7.25963, 80.59915)
    map_widget.set_zoom(20)
    return map_widget

def load_images():
    current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    location_skyc = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "location_skyc.png")).resize((5, 8)))
    location_drone = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "location_drones.png")).resize((5, 8)))
    return location_skyc, location_drone

def add_marker_event(coords, showOrientationVal, map_widget, location_skyc, drone_home_positions, markers_skyc):
    print("Add marker:", coords)
    print(drone_home_positions)
        
    lat1_1 = coords[0]
    lon1_1 = coords[1]

    for marker in markers_skyc:
        marker.delete()
    markers_skyc.clear()

    for i, position in enumerate(drone_home_positions, 1):
        print(f"Drone {i}: {position}")
        distance, bearing = calculate_distance_and_bearing(drone_home_positions[0][:2], position[:2])
        print(distance, bearing)
        lat, lon = get_point_at_distance(lat1_1, lon1_1, distance/1000, bearing+showOrientationVal)
        markers_skyc.append(map_widget.set_marker(lat, lon, icon=location_skyc, icon_anchor="s", text=i, text_color="#000000", font="Tahoma 6 bold"))



def extract_skycfile_and_parse_jsondata(zip_file_path, json_file_name):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # Check if the JSON file exists in the zip file
        if json_file_name in zip_file.namelist():
            # Extract the JSON file from the zip file
            with zip_file.open(json_file_name) as json_file:
                # Read and parse the JSON data
                data = json.load(json_file)
                return data



def upload_file(markers_skyc, drone_home_positions, showOrigin, showOrientation, label, map_widget, location_skyc):
    for marker in markers_skyc:
        marker.delete()
    markers_skyc.clear()

    contentShowOrientation = showOrientation.get()
    float_contentShowOrientation = float(contentShowOrientation)
    showOrientationVal = float_contentShowOrientation
    print(showOrientationVal)

    contentShowOrigin = showOrigin.get()
    print(showOrientationVal)

    lat1_1_str, lon1_1_str = contentShowOrigin.split()
    lat1_1 = float(lat1_1_str)
    lon1_1 = float(lon1_1_str)

    skyc_file_path = filedialog.askopenfilename()
    json_file_name = 'show.json'

    if skyc_file_path:
        label.config(text=skyc_file_path)
        drone_home_positions.clear()

        data = extract_skycfile_and_parse_jsondata(skyc_file_path, json_file_name)

        for drone in data['swarm']['drones']:
            home_position = drone['settings']['home']
            drone_home_positions.append(home_position)

        # Now, 'drone_home_positions' contains a list of home positions
        print("Home Positions of Drones:")
        for i, position in enumerate(drone_home_positions, 1):
            print(f"Drone {i}: {position}")
            distance, bearing = calculate_distance_and_bearing(drone_home_positions[0][:2], position[:2])
            print(distance, bearing)
            lat, lon = get_point_at_distance(lat1_1, lon1_1, distance/1000, bearing)
            markers_skyc.append(map_widget.set_marker(lat, lon, icon=location_skyc, icon_anchor="s", text=i, text_color="#000000", font="Tahoma 6 bold"))

    else:
        for marker in markers_skyc:
            marker.delete()
        markers_skyc.clear()
        label.config(text="No file selected")

