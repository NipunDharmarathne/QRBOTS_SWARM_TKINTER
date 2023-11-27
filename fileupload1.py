import tkinter as tk
from tkinter import filedialog
import json
import math

def calculate_distance_and_bearing(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    angle = math.atan2(x2 - x1, y2 - y1)
    angle_degrees = math.degrees(angle)
    return distance, angle_degrees

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text="File Selected: " + file_path)

        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract home positions of drones
        drone_home_positions = []

        for drone in data['swarm']['drones']:
            home_position = drone['settings']['home']
            drone_home_positions.append(home_position)

        # Now, 'drone_home_positions' contains a list of home positions
        print("Home Positions of Drones:")
        for i, position in enumerate(drone_home_positions, 1):
            print(f"Drone {i}: {position}")
            print(f"Drone {i}: {calculate_distance_and_bearing(drone_home_positions[0][:2], position[:2])}")

    else:
        label.config(text="No file selected")

# Create the main window
root = tk.Tk()
root.title("File Upload Example")

# Create a label to display the selected file path
label = tk.Label(root, text="No file selected", padx=10, pady=10)
label.pack()

# Create a button to trigger the file dialog
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
