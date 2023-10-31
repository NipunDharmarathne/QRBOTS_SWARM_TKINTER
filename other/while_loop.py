import tkinter as tk

def start_loop():
    global running
    running = True
    run_loop()

def stop_loop():
    global running
    running = False

def run_loop():
    if running:
        # Your loop code here
        print("Running...")
        root.after(500, run_loop)  # Repeat the function every 1000 ms (1 second)

running = False

# Create the main tkinter window
root = tk.Tk()
root.title("Start/Stop Loop")

# Create buttons to start and stop the loop
start_button = tk.Button(root, text="Start Loop", command=start_loop)
stop_button = tk.Button(root, text="Stop Loop", command=stop_loop)

start_button.pack()
stop_button.pack()

# Start the tkinter main loop
root.mainloop()
