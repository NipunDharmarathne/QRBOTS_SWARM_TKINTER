import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Separate Sections with Buttons and Labels")

# Create a Frame for the buttons section
buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create buttons in the buttons section
button1 = tk.Button(buttons_frame, text="Button 1")
button2 = tk.Button(buttons_frame, text="Button 2")
button1.pack(pady=5)
button2.pack(pady=5)

# Create a Frame for the labels section
labels_frame = tk.Frame(root)
labels_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create labels in the labels section
label1 = tk.Label(labels_frame, text="Label 1")
label2 = tk.Label(labels_frame, text="Label 2")
label1.pack(pady=5)
label2.pack(pady=5)

# Start the Tkinter main loop
root.mainloop()
