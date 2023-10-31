import tkinter as tk
from tkinter import Scrollbar

root = tk.Tk()
root.title("Scrollable Label")

# Create a Canvas to hold the label and allow scrolling
canvas = tk.Canvas(root, width=300, height=150)
canvas.pack()

# Create a Frame to contain the label and add it to the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Create a Scrollbar and attach it to the canvas
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create the Label with a long text
label_text = "This is a long text that can be scrolled vertically in a Label widget in Tkinter. " * 100
label = tk.Label(frame, text=label_text, wraplength=280, justify="left")
label.pack()

# Update the canvas to display the entire label
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
