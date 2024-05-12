from flask import Blueprint, jsonify, request
import subprocess
import os
import datetime
from utils.nmap_2_json import convert_xml_to_json

# Initialize the Blueprint
scan = Blueprint('scan', __name__)

JSON_BASE_FOLDER = 'scan_results/'


@scan.route("/", methods=['POST'])
def start_scan():
    # Get IP address from the form data
    target_ip = request.form.get('ip')
    if not target_ip:
        return jsonify({"error": "No IP address provided"}), 400

    # Ensure the directory for this IP exists
    directory_path = os.path.join(JSON_BASE_FOLDER, target_ip)
    os.makedirs(directory_path, exist_ok=True)
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the file path for the XML output with timestamp
    xml_output_path = os.path.join(directory_path, f"{current_time}.xml")

    command = f"nmap -sV --script vulners.nse {target_ip} -oX {xml_output_path}"

    try:
        # Run the nmap command
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        json_output_filename = convert_xml_to_json(xml_output_path)

        if json_output_filename:
            return jsonify({"message": f"Scan and conversion successful, results saved in {json_output_filename}"})
        else:
            return jsonify({"error": "Failed to convert scan result to JSON"}), 500

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to execute scan on {target_ip}. Error: {str(e)}"}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to execute scan on {target_ip}. Error: {str(e)}"}), 500
