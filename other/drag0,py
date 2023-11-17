import tkinter as tk

def on_press(event):
    item = canvas.find_closest(event.x, event.y)[0]
    drag_data["item"] = item
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def on_drag(event):
    delta_x = event.x - drag_data["x"]
    delta_y = event.y - drag_data["y"]
    canvas.move(drag_data["item"], delta_x, delta_y)
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def on_release(event):
    drag_data["item"] = None

def main():
    global canvas, drag_data
    root = tk.Tk()
    root.title("Draggable Point Example")

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    drag_data = {"x": 0, "y": 0, "item": None}

    circle = canvas.create_oval(195, 195, 205, 205, fill="red", tags="draggable")

    # Bind mouse events to functions
    canvas.tag_bind("draggable", "<ButtonPress-1>", on_press)
    canvas.tag_bind("draggable", "<B1-Motion>", on_drag)
    canvas.tag_bind("draggable", "<ButtonRelease-1>", on_release)

    root.mainloop()

if __name__ == "__main__":
    main()
