from tkinter import *

master = Tk()
master.configure(bg="grey6")
master.title("QRBOTS")

# this will create a label widget
l1 = Label(master, text = "Number of Drones:", fg="white", bg="grey6")
l2 = Label(master, text = "0", fg="white", bg="grey6")
l1.grid(row = 0, column = 0, sticky = E)
l2.grid(row = 0, column = 1, sticky = W)

# Create a Text widget for displaying text
text = Text(master, wrap="word", width=27, height=5)
text.grid(row = 1, column=0, columnspan=2)
label_text = "This is a long text that can be scrolled vertically in a Label widget in Tkinter.\n" * 10
text.insert("1.0", label_text)


scan = Button(master, text = "SCAN", bg="springgreen3")
stop = Button(master, text = "STOP", bg="tomato")
master.rowconfigure(2, minsize=35)
scan.grid(row = 2, column=0, sticky = "E")
stop.grid(row = 2, column=1, sticky = "W")

# button widget
b1 = Button(master, text = "ARM ALL", height=3, width=15, bg="springgreen3")
b2 = Button(master, text = "DISARM ALL", height=3, width=15, bg="cyan3")
b3 = Button(master, text = "HOLD ALL", height=3, width=15, bg="olivedrab1")
b4 = Button(master, text = "RTH ALL", height=3, width=15, bg="chocolate1")
b5 = Button(master, text = "LAND ALL", height=3, width=15, bg="goldenrod1")
b6 = Button(master, text = "SHUTDOWN ALL", height=3, width=15, bg="tomato")

# arranging button widgets
b1.grid(row = 3, column = 0, sticky = W)
b2.grid(row = 3, column = 1, sticky = W)
b3.grid(row = 4, column = 0, sticky = W)
b4.grid(row = 4, column = 1, sticky = W)
b5.grid(row = 5, column = 0, sticky = W)
b6.grid(row = 5, column = 1, sticky = W)

mainloop()
