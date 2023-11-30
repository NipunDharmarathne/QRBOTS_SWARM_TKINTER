from tkinter import Tk, Entry

# Create the main window
master = Tk()

# Create a single-line text widget (Entry)
singleLineText = Entry(master, width=22)

# Pack the widget into the main window
singleLineText.pack()

# Start the Tkinter event loop
master.mainloop()
