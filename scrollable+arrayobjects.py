from tkinter import *

def create_labels_and_buttons(frame):
    for i in range(25):
        label = Label(frame, text=f"Label {i}")
        button = Button(frame, text=f"Button {i}")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        button.grid(row=i, column=1, padx=10, pady=5, sticky="e")

def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

root = Tk()
root.title("Scrollable Area")

# Create a frame for the canvas and scrollbar
frame = Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

# Specify the width and height for the canvas
canvas = Canvas(frame, width=300, height=200)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas.config(yscrollcommand=scrollbar.set)

frame_inner = Frame(canvas)
canvas.create_window((0, 0), window=frame_inner, anchor="nw")
create_labels_and_buttons(frame_inner)

frame_inner.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

canvas.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()
