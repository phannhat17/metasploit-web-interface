from flask import Flask, render_template, request, jsonify
from pymetasploit3.msfrpc import MsfRpcClient

app = Flask(__name__)

# Initialize Metasploit connection
def init_metasploit():
    client = MsfRpcClient('yourpassword', port=55553, ssl=True)
    return client

@app.route('/')
def index():
    client = init_metasploit()
    search_query = request.args.get('query', '')
    results = client.modules.search(search_query)
    total = len(results)

    return render_template('index.html', rows=results, total=total)

# @app.route('/search', methods=['GET'])
# def search():
#     client = init_metasploit()
#     search_query = request.args.get('query', '')
#     results = client.modules.search(search_query)

#     return render_template('index.html', rows=results)

#     # return jsonify(formatted_results)

@app.route('/module_details')
def module_details():
    client = init_metasploit()
    module_type, module_name = request.args.get('module_type'), request.args.get('module_name')
    exploit = client.modules.use(module_type, module_name)
    return jsonify({'description': exploit.description, 'options': exploit.options})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
