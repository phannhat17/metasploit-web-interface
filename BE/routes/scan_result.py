from flask import Blueprint, jsonify, request
import json
import os
import datetime
from utils.load_json import load_json_file

# Initialize the Blueprint
scanres = Blueprint('scanres', __name__)

JSON_BASE_FOLDER = 'scan_results/'

@scanres.route('/', methods=['GET'])
def scan_res():
    """
    Return the entire JSON data for a given timestamp and IP address.
    """
    
    ip = request.args.get('ip')
    timestamp = request.args.get('timestamp')
    result_type = request.args.get('resulttype')
    portid = request.args.get('portid')

    if not ip or not timestamp or not result_type:
        return jsonify({"error": "Missing required parameters (ip, timestamp, or resulttype)"}), 400

    data = load_json_file(timestamp, ip)
    if not data:
        return jsonify({"error": f"Not found the scan result for {timestamp} at {ip}"}), 404

    if portid:
        host_data = data.get('host', {})
        ports = host_data.get('ports', {}).get('port', None)
        

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

        scan_time = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        
        if ports:
            return jsonify({"ports": ports, "ip": ip, "timestamp": timestamp, "scan_time": scan_time})
        else:
            return jsonify({"error": "Port key not found under Host in the JSON data"}), 404
    
    else:
        return jsonify({"error": "Invalid result type provided"}), 400

@scanres.route('/all-record', methods=['GET'])
def all_record():
    """
    Returns a list of all directories within the base folder or files of a specific IP if the 'ip' query parameter is provided.
    """
    target_ip = request.args.get('ip')  # Get the IP address from query parameter

    try:
        if target_ip:
            # Path for the specific IP directory
            ip_path = os.path.join(JSON_BASE_FOLDER, target_ip)
            if os.path.exists(ip_path) and os.path.isdir(ip_path):
                # List files in the directory for the specific IP
                files = os.listdir(ip_path)
                files_detail = [
                    {
                        "timestamp": file.split(".")[0],
                        "formatted_time": datetime.datetime.strptime(file.split(".")[0], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                    }
                    for file in files if os.path.isfile(os.path.join(ip_path, file))
                ]
                return jsonify({"ip": target_ip, "records": files_detail})
            else:
                return jsonify({"error": f"No records found for IP: {target_ip}"}), 404
        else:
            # List all items in the base directory
            items = os.listdir(JSON_BASE_FOLDER)
            directories = []
            for item in items:
                item_path = os.path.join(JSON_BASE_FOLDER, item)
                if os.path.isdir(item_path):
                    # List the contents of the directory
                    subitems = os.listdir(item_path)
                    # Count how many of these are files
                    file_count = sum(1 for subitem in subitems if os.path.isfile(os.path.join(item_path, subitem)))
                    directories.append({"ip": item, "scans": file_count})
            return jsonify({"directories": directories})
    except Exception as e:
        # Handle errors such as missing directory or permission issues
        return jsonify({"error": str(e)}), 500

@scanres.route('/script-details', methods=['GET'])
def get_script_details():
    """
    Return the script details for a specific port.
    """
    ip = request.args.get('ip')
    timestamp = request.args.get('timestamp')
    portid = request.args.get('portid')

    if not ip or not timestamp or not portid:
        return jsonify({"error": "Missing required parameters (ip, timestamp, or portid)"}), 400

    data = load_json_file(timestamp, ip)
    if not data:
        return jsonify({"error": f"Not found the scan result for {timestamp} at {ip}"}), 404

    host_data = data.get('host', {})
    ports = host_data.get('ports', {}).get('port', [])

    # Ensure ports is a list
    if not isinstance(ports, list):
        ports = [ports]

    for port in ports:
        if port.get('@portid') == portid and 'script' in port:
            return jsonify(port['script'])

    return jsonify({"error": "Script data not found for port"}), 404
