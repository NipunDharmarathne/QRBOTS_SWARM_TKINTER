import tkinter as tk

class DraggablePoint:
    def __init__(self, canvas, x, y, radius=5, color="red"):
        self.canvas = canvas
        self.circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, tags="draggable")
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Bind mouse events
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = item
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_release(self, event):
        self.drag_data["item"] = None

def main():
    root = tk.Tk()
    root.title("Draggable Point Example")

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    draggable_point = DraggablePoint(canvas, 200, 200)

    root.mainloop()

if __name__ == "__main__":
    main()
