import tkinter as tk

class Point:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.circle = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", tags="point")
        self.canvas.tag_bind("point", "<B1-Motion>", self.move)

    def move(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.circle, x - 5, y - 5, x + 5, y + 5)

def main():
    root = tk.Tk()
    root.title("Moveable Points")

    canvas = tk.Canvas(root, width=300, height=300, bg="white")
    canvas.pack()

    points = [Point(canvas, 50, 50), Point(canvas, 50, 100), Point(canvas, 50, 150)]

    root.mainloop()

if __name__ == "__main__":
    main()
