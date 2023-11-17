import tkinter as tk

class PointMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point Mover")

        # Initialize points
        self.points = [(0, 0), (0, 5), (0, 10)]
        self.point_radius = 5

        # Create canvas to display points
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw initial points
        self.draw_points()

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.move_point)

    def draw_points(self):
        self.canvas.delete("all")  # Clear previous drawings
        for point in self.points:
            x, y = point
            self.canvas.create_oval(x - self.point_radius, y - self.point_radius,
                                     x + self.point_radius, y + self.point_radius,
                                     fill="blue", outline="black")

    def move_point(self, event):
        for i, point in enumerate(self.points):
            x, y = point
            if (x - self.point_radius) <= event.x <= (x + self.point_radius) and \
                    (y - self.point_radius) <= event.y <= (y + self.point_radius):
                # Update the selected point's position
                self.points[i] = (event.x, event.y)
                self.draw_points()  # Redraw points after moving
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = PointMoverApp(root)
    root.mainloop()
