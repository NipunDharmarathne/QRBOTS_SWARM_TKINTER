import tkinter as tk
from tkinter import ttk

class ZoomableFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.scale_factor = 1.0

        # Bind mouse wheel events for zooming
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        # Add some content to the frame (for demonstration purposes)
        self.label = ttk.Label(self.canvas, text="Zoomable Frame Content")
        self.label_id = self.canvas.create_window(50, 50, window=self.label, anchor=tk.NW)

    def on_mousewheel(self, event):
        # Zoom in or out based on the direction of the mouse wheel scroll
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def zoom_in(self):
        self.scale_factor *= 1.1  # Increase the scale factor
        self.update_content_scale()

    def zoom_out(self):
        self.scale_factor /= 1.1  # Decrease the scale factor
        self.update_content_scale()

    def update_content_scale(self):
        # Update the scale of the canvas content
        self.canvas.scale("all", 0, 0, self.scale_factor, self.scale_factor)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Zoomable Frame Example")

    zoomable_frame = ZoomableFrame(root, width=400, height=300)
    zoomable_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
