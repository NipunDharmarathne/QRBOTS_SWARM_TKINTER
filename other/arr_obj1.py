import tkinter as tk

def button_click(label):
    label.config(text="Button Clicked!")

root = tk.Tk()
root.title("Button and Label Array")

# Create an array to hold button and label pairs
button_label_pairs = []

# Create and add button and label pairs to the array
for i in range(5):
    frame = tk.Frame(root)
    frame.pack()
    
    label = tk.Label(frame, text="Label " + str(i))
    label.pack(side="left")
    
    button = tk.Button(frame, text="ARM", command=lambda label=label: button_click(label))
    button.pack(side="left")

    button_label_pairs.append((button, label))

root.mainloop()
