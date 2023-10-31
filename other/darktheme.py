import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("QRBOTS")

# Customize the title bar color (black) and content color (white)
root.configure(bg="black")  # Set the title bar color to black
root.option_add("*TButton*highlightColor", "white")  # Set the content color to white for TButtons
root.option_add("*TEntry*highlightColor", "white")   # Set the content color to white for TEntries

# Create and add widgets to the window
label = tk.Label(root, text="Hello, QRBOTS!", fg="white", bg="black")
label.pack()

button = tk.Button(root, text="Click Me", fg="white", bg="black")
button.pack()

# Run the Tkinter main loop
root.mainloop()
