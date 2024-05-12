from flask import Flask, render_template, request, jsonify
# from pymetasploit3.msfrpc import *
import os
from threading import Thread
from queue import Queue
import time
import itertools
from routes.scan_result import scanres

app = Flask(__name__)
app.register_blueprint(scanres, url_prefix='/scanres')

# msfpass = os.getenv('MSFPASS', 'yourpassword')  

# client = MsfRpcClient(msfpass, port=55553, ssl=True)


# def perform_scan(target_ip, scan_type, output):
#     console = client.consoles.console()
#     console.write('workspace')
#     time.sleep(1)  # Give it some time to respond
#     db_status = console.read()['data']

#     # Perform the nmap scan and wait for it to complete
#     console.write(f'db_nmap {scan_type} {target_ip}')
#     loading = itertools.cycle(['-', '\\', '|', '/'])  # Loading animation sequence
#     data = ''
#     timer = 0
#     print("Monitoring scan progress...", end="")
#     while data == '' or console.is_busy():
#         time.sleep(1)  # Interval to wait before checking console output
#         new_data = console.read()['data']
#         if new_data:
#             data += new_data
#             # Instead of printing each new data, you might just want to print it if it's meaningful, or log it to a file.
#         else:
#             print(f"\rMonitoring scan progress... {next(loading)}", end="", flush=True)  # Update the animation
#         timer += 1
#         if timer > 300:  # Timeout to prevent infinite loop
#             print("\nScan timed out")
#             break
#     print("\nScan completed.")

#     # Fetch and print vulnerabilities found after scan
#     console.write('vulns')
#     time.sleep(2)  # Wait for the command to complete
#     vulns_data = console.read()['data']
#     if not vulns_data:
#         vulns_data = "No vulnerabilities found."

#     print(vulns_data)

#     console.destroy()
#     output.put(vulns_data)  # Only return the vulnerabilities data

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         name = request.form.get('name', '')
#         m_type = request.form.get('type', None) 

#         search_parts = []
#         if name:
#             search_parts.append("name:" + name)
#         if m_type and m_type != 'all':
#             search_parts.append("type:" + m_type)

#         search_query = ' '.join(search_parts)
#         if search_query == '':
#             results = []
#             return render_template('index.html', toast=True, rows=results, filter_type=m_type)
#         elif "type" not in search_query:
#             results = client.modules.search(search_query)
#             return render_template('index.html', toast2=True, rows=results, filter_type=m_type)
#         else:
#             results = client.modules.search(search_query)
#             return render_template('index.html', rows=results, filter_type=m_type)

#     return render_template('index.html')

# @app.route('/adv_search', methods=['GET', 'POST'])
# def adv_search():
#     if request.method == 'POST':
#         name = request.form.get('name', None)
#         fullname = request.form.get('fullname', None)
#         aka = request.form.get('aka', None)
#         date = request.form.get('date', None)
#         target = request.form.get('target', None)
#         author = request.form.get('author', None)
#         m_type = request.form.get('type', None)
#         platform = request.form.get('platform', None)
#         arch = request.form.get('arch', None)
#         path = request.form.get('path', None)
#         port = request.form.get('port', None)
#         edb = request.form.get('edb', None)
#         bid = request.form.get('bid', None)
#         cve = request.form.get('cve', None)
#         reference = request.form.get('reference', None)
#         rank = request.form.get('rank', None)
#         check = request.form.get('check', 'false')

#         search_parts = []
#         if name:
#             search_parts.append("name:" + name)
#         if fullname:
#             search_parts.append("fullname:" + fullname)
#         if aka:
#             search_parts.append("aka:" + aka)
#         if date:
#             search_parts.append("date:" + date)
#         if target:
#             search_parts.append("target:" + target)
#         if author:
#             search_parts.append("author:" + author)
#         if m_type and m_type != 'all':
#             search_parts.append("type:" + m_type)
#         if platform:
#             search_parts.append("platform:" + platform)
#         if arch:
#             search_parts.append("arch:" + arch)
#         if path:
#             search_parts.append("path:" + path)
#         if port:
#             search_parts.append("port:" + port)
#         if edb:
#             search_parts.append("edb:" + edb)
#         if bid:
#             search_parts.append("bid:" + bid)
#         if cve:
#             search_parts.append("cve:" + cve)
#         if reference:
#             search_parts.append("reference:" + reference)
#         if rank:
#             search_parts.append("rank:" + rank)
#         if check != 'None':
#             search_parts.append("check:" + check)

#         search_query = ' '.join(search_parts)
#         if search_query == '':
#             results = []
#             return render_template('adv_search.html', toast=True, rows=results, filter_type=m_type)
#         elif "type" not in search_query:
#             results = client.modules.search(search_query)
#             return render_template('adv_search.html', toast2=True, rows=results, filter_type=m_type)
#         else:
#             results = client.modules.search(search_query)
#             return render_template('adv_search.html', rows=results, filter_type=m_type)
#     else:
#         return render_template('adv_search.html')


# @app.route('/module_details')
# def module_details():
#     module_type, module_name = request.args.get('module_type'), request.args.get('module_name')
#     exploit = client.modules.use(module_type, module_name)
#     return jsonify(exploit.info)
    
# @app.route('/scan', methods=['GET', 'POST'])
# def scan():
#     if request.method == 'POST':
#         target_ip = request.form.get('target_ip', '')
#         scan_type = request.form.get('scan_type', '-sV')

#         if target_ip:
#             # Create a queue to hold the scan results
#             output = Queue()

#             # Start the scan in a background thread
#             thread = Thread(target=perform_scan, args=(target_ip, scan_type, output))
#             thread.start()

#             # Wait for the thread to complete and get results
#             thread.join()
#             scan_results = output.get()

#             # Render the scan results in the template
#             return render_template('scan_results.html', scan_results=scan_results)
#         else:
#             return render_template('scan.html', error="Please specify a target IP")

#     return render_template('scan.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
