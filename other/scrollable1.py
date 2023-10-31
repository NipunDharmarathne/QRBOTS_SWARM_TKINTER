import tkinter as tk

root = tk.Tk()
root.title("Scrollable Label")

# Create a Text widget for displaying text
text = tk.Text(root, wrap="word", width=40, height=10)
text.pack()



# Insert the long text into the Text widget
label_text = "This is a long text that can be scrolled vertically in a Label widget in Tkinter. " * 10
text.insert("1.0", label_text)

root.mainloop()
