import tkinter as tk

def create_labels_and_buttons(frame):
    for i in range(5):
        label = tk.Label(frame, text=f"Label {i}")
        button = tk.Button(frame, text=f"Button {i}")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        button.grid(row=i, column=1, padx=10, pady=5, sticky="e")

root = tk.Tk()
root.title("Scrollable Area")

# Set the fixed width and height for the canvas
canvas = tk.Canvas(root, width=400, height=200)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

# Set the fixed width for the frame and disable resizing
frame = tk.Frame(canvas, width=400)
frame.pack_propagate(0)
canvas.create_window((0, 0), window=frame, anchor="nw")
create_labels_and_buttons(frame)

frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
