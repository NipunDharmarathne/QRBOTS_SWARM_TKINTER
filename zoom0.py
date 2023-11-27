import tkinter as tk

class ZoomableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.bind("<Control-plus>", self.zoom_in)

    def zoom_in(self, event):
        scale_factor = 1.2
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)
        self.config(scrollregion=self.bbox("all"), width=new_width, height=new_height)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Zoomable Canvas")

    canvas = ZoomableCanvas(root, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Add some content to the canvas (you can customize this part)
    canvas.create_rectangle(50, 50, 150, 150, fill="blue")

    root.mainloop()
