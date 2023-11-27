import tkinter as tk
from tkinter import filedialog
import json
import zipfile

def upload_file():
    zip_file_path = filedialog.askopenfilename()
    json_file_name = 'show.json'

    if zip_file_path:
        label.config(text="File Selected: " + zip_file_path)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            # Check if the JSON file exists in the zip file
            if json_file_name in zip_file.namelist():
                # Extract the JSON file from the zip file
                with zip_file.open(json_file_name) as json_file:
                    # Read and parse the JSON data
                    json_data = json.load(json_file)
                    
                    # Now you can work with the JSON data
                    print(json_data)

    else:
        label.config(text="No file selected")

# Create the main window
root = tk.Tk()
root.title("File Upload Example")

# Create a label to display the selected file path
label = tk.Label(root, text="No file selected", padx=10, pady=10)
label.pack()

# Create a button to trigger the file dialog
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
