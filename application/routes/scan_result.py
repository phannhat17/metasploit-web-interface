from flask import Blueprint, jsonify, request
import json
import os

# Initialize the Blueprint
scanres = Blueprint('scanres', __name__)
 
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
 
@scanres.route('/scan-result', methods=['GET'])
def scan_res():
    """
    Return the entire JSON data for a given timestamp and IP address.
    """
    
    ip = request.args.get('ip')
    timestamp = request.args.get('timestamp')
    result_type = request.args.get('resulttype')

    if not ip or not timestamp or not result_type:
        return jsonify({"error": "Missing required parameters (ip, timestamp, or resulttype)"}), 400

    data = load_json_file(timestamp, ip)
    if not data:
        return jsonify({"error": f"Not found the scan result for {timestamp} at {ip}"}), 404
 
    if result_type == "all":
        return jsonify(data)

    elif result_type == "run_stat":
        runstats = data.get("runstats", {})
        finished_data = runstats.get('finished', {})
        time_str = finished_data.get('@timestr')
        exit_status = finished_data.get('@exit')
 
        if time_str and exit_status:
            return jsonify({"TimeStr": time_str, "Exit": exit_status})
        else:
            return jsonify({"error": "TimeStr or Exit fields not found in the Finished section"}), 404
    
    elif result_type == "port":
        host_data = data.get('host', {})
        ports = host_data.get('ports', {}).get('port', None)
        
        if ports:
            return jsonify({"Port": ports})
        else:
            return jsonify({"error": "Port key not found under Host in the JSON data"}), 404
    
    else:
        return jsonify({"error": "Invalid result type provided"}), 400
