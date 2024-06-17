from flask import Blueprint, jsonify, request, render_template
import subprocess
import os
import datetime
from utils.nmap_2_json import convert_xml_to_json

# Initialize the Blueprint
scan = Blueprint('scan', __name__)

JSON_BASE_FOLDER = 'scan_results/'


# @scan.route("/", methods=['POST', 'GET'])
# def start_scan():
#     if request.method == 'POST':

#         # Get IP address from the form data
#         target_ip = request.form.get('ip')
#         if not target_ip:
#             return jsonify({"error": "No IP address provided"}), 400

#         # Ensure the directory for this IP exists
#         directory_path = os.path.join(JSON_BASE_FOLDER, target_ip)
#         os.makedirs(directory_path, exist_ok=True)
#         current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

#         # Define the file path for the XML output with timestamp
#         xml_output_path = os.path.join(directory_path, f"{current_time}.xml")

#         command = f"nmap -sV -p- --script vulners.nse {target_ip} -oX {xml_output_path}"

#         try:
#             # Run the nmap command
#             subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             json_output_filename = convert_xml_to_json(xml_output_path)

#             if json_output_filename:
#                 return render_template('scan.html', success="Scan and conversion successful!")
#                 # return jsonify({"message": f"Scan and conversion successful!"})
#             else:
#                 return render_template('scan.html', error="Failed to convert scan result to JSON!")
#                 # return jsonify({"error": "Failed to convert scan result to JSON"}), 500

#         except subprocess.CalledProcessError as e:
#             return render_template('scan.html', error="Failed to execute scan!")
#             # return jsonify({"error": f"Failed to execute scan on {target_ip}. Error: {str(e)}"}), 500
#     else:
#         return render_template('scan.html')

@scan.route("/start_scan", methods=['POST'])
def start_scan():
    data = request.json
    target_range = data.get('ip_range')
    if not target_range:
        return jsonify({"error": "No IP address or range provided"}), 400

    auto_scan_services = data.get('auto_scan_services', False)
    auto_scan_os = data.get('auto_scan_os', False)

    directory_path = os.path.join(JSON_BASE_FOLDER, target_range.replace("/", "_"))
    os.makedirs(directory_path, exist_ok=True)
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    xml_output_path = os.path.join(directory_path, f"{current_time}.xml")

    command = f"nmap -sV -p- {target_range} -oX {xml_output_path}"
    if auto_scan_os:
        command += " -O"
    if auto_scan_services:
        command += " --script vulners.nse"

    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        json_output_filename = convert_xml_to_json(xml_output_path)
        if json_output_filename:
            return jsonify({"success": "Scan and conversion successful!"})
        else:
            return jsonify({"error": "Failed to convert scan result to JSON!"}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to execute scan!"}), 500
