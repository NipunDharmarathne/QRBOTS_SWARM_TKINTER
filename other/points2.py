import tkinter as tk

class MovablePoint:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", tags="point")
        self.drag_data = {"x": 0, "y": 0, "item": None}

        canvas.tag_bind("point", "<ButtonPress-1>", self.on_press)
        canvas.tag_bind("point", "<B1-Motion>", self.on_drag)

    def on_press(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

def main():
    root = tk.Tk()
    root.title("Movable Points")

    canvas = tk.Canvas(root, width=300, height=300, bg="white")
    canvas.pack()

    points = [
        MovablePoint(canvas, 50, 50),
        MovablePoint(canvas, 150, 150),
        MovablePoint(canvas, 250, 250),
    ]

    root.mainloop()

if __name__ == "__main__":
    main()
