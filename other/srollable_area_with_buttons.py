import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Scrollable Area with Buttons")

# Create a Canvas widget for the scrollable area
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar and connect it to the canvas
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the buttons
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Create buttons and add them to the frame
for i in range(20):  # Create 20 buttons as an example
    button = tk.Button(frame, text=f"Button {i + 1}")
    button.pack(pady=5)

# Function to update the canvas scrolling region
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the update_scroll_region function to the frame and canvas resizing events
frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", update_scroll_region)

root.mainloop()
