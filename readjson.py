import json

# Specify the path to your JSON file
file_path = 'path/to/your/file.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Now, 'data' contains the parsed JSON content
print(data)