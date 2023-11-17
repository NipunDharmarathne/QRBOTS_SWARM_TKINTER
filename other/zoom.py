import tkinter as tk
from tkinter import ttk
import tkintermapview

class ZoomableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scale_factor = 1.0

    def _on_mousewheel(self, event):
        # Respond to mouse wheel event to zoom in/out
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale("all", event.x, event.y, factor, factor)
        self.scale_factor *= factor

def main():
    root = tk.Tk()
    root.title("Zoomable Window")

    zoomable_canvas = ZoomableCanvas(root, width=400, height=300, background="white")
    zoomable_canvas.pack(fill=tk.BOTH, expand=True)

    # Add some content to the canvas (optional)
    zoomable_canvas.create_rectangle(50, 50, 150, 150, fill="blue")
  
    root.mainloop()

if __name__ == "__main__":
    main()
