from flask import Flask, render_template, request, jsonify
from pymetasploit3.msfrpc import MsfRpcClient

app = Flask(__name__)

# Initialize Metasploit connection
def init_metasploit():
    client = MsfRpcClient('yourpassword', port=55553, ssl=True)
    return client

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    client = init_metasploit()
    search_query = request.args.get('query', '')

    # Use the client.modules.search function to search for modules
    # This function returns modules matching the search query across all types
    results = client.modules.search(search_query)

    # Format results to make them easily consumable by the front-end
    formatted_results = [{
        'type': result['type'],
        'name': result['name'],
        'fullname': result['fullname'],
        'rank': result['rank'],
        'disclosuredate': result['disclosuredate']
    } for result in results]

    return jsonify(formatted_results)

@app.route('/module_details')
def module_details():
    client = init_metasploit()
    module_type, module_name = request.args.get('module_type'), request.args.get('module_name')
    exploit = client.modules.use(module_type, module_name)
    return jsonify({'description': exploit.description, 'options': exploit.options})

if __name__ == '__main__':
    app.run(debug=True)
