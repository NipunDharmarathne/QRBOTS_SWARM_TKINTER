import tkinter as tk

def on_enter(event):
    user_input = entry.get()
    print("User entered:", user_input)

# Create the main window
root = tk.Tk()
root.title("Entry Box Example")

# Create an Entry widget
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Bind the Enter key event to the on_enter function
entry.bind("<Return>", on_enter)

# Run the Tkinter event loop
root.mainloop()
