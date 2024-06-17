import json
import os

# Base folder where all scan results are stored
JSON_BASE_FOLDER = 'scan_results/'
 
def load_json_file(timestamp, ip):
    """
    Load the JSON file based on the timestamp and IP.
    Returns the loaded JSON data if the file is found, otherwise returns None.
    """
    # Construct the folder path based on the IP address directly
    ip_folder_path = os.path.join(JSON_BASE_FOLDER, ip)
 
    # Construct the full path to the specific JSON file
    json_file_name = f"{timestamp}.json"
    json_file_path = os.path.join(ip_folder_path, json_file_name)
 
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            # Load the JSON file contents
            return json.load(file).get("nmaprun")
    else:
        # Log the missing file path for debugging
        print(f"File not found: {json_file_path}", flush=True)
        return None