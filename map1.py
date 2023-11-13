import tkinter as tk

# Create a main window
root = tk.Tk()
root.title("Simple Map")

# Create a Canvas widget to display the map
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a rectangle on the canvas to represent a building or landmark
canvas.create_rectangle(50, 50, 150, 150, fill="blue")
canvas.create_text(100, 100, text="Landmark")

# Create lines to represent roads or paths
canvas.create_line(30, 200, 200, 200, fill="black", width=3)
canvas.create_line(200, 200, 200, 350, fill="black", width=3)

# Create an oval to represent a park or lake
canvas.create_oval(250, 250, 350, 350, fill="green")
canvas.create_text(300, 300, text="Park")

# Run the tkinter main loop
root.mainloop()
