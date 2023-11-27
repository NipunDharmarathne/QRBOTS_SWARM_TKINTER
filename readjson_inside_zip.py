import zipfile
import json

skyc_file_path = 'your_zip_file.zip'
json_file_name = 'your_json_file.json'

with zipfile.ZipFile(skyc_file_path, 'r') as zip_file:
    # Check if the JSON file exists in the zip file
    if json_file_name in zip_file.namelist():
        # Extract the JSON file from the zip file
        with zip_file.open(json_file_name) as json_file:
            # Read and parse the JSON data
            json_data = json.load(json_file)
            
            # Now you can work with the JSON data
            print(json_data)
    else:
        print(f"{json_file_name} not found in the zip file.")