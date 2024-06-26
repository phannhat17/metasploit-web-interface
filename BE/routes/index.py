from flask import Blueprint, render_template, request, jsonify
from .msf_client import client
import os

# Initialize the Blueprint
index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['POST'])
def search():
    data = request.get_json()
    name = data.get('name', '')
    m_type = data.get('type', None)

    search_parts = []
    if name:
        search_parts.append("name:" + name)
    if m_type and m_type != 'all':
        search_parts.append("type:" + m_type)

    search_query = ' '.join(search_parts)
    if search_query == '':
        results = []
        return jsonify({'toast': True, 'rows': results})
    elif "type" not in search_query:
        results = client.modules.search(search_query)
        return jsonify({'toast2': True, 'rows': results})
    else:
        results = client.modules.search(search_query)
        return jsonify({'rows': results})

@index_bp.route('/adv_search', methods=['GET', 'POST'])
def adv_search():
    if request.method == 'POST':
        name = request.form.get('name', None)
        fullname = request.form.get('fullname', None)
        aka = request.form.get('aka', None)
        date = request.form.get('date', None)
        target = request.form.get('target', None)
        author = request.form.get('author', None)
        m_type = request.form.get('type', None)
        platform = request.form.get('platform', None)
        arch = request.form.get('arch', None)
        path = request.form.get('path', None)
        port = request.form.get('port', None)
        edb = request.form.get('edb', None)
        bid = request.form.get('bid', None)
        cve = request.form.get('cve', None)
        reference = request.form.get('reference', None)
        rank = request.form.get('rank', None)
        check = request.form.get('check', 'false')

        search_parts = []
        if name:
            search_parts.append("name:" + name)
        if fullname:
            search_parts.append("fullname:" + fullname)
        if aka:
            search_parts.append("aka:" + aka)
        if date:
            search_parts.append("date:" + date)
        if target:
            search_parts.append("target:" + target)
        if author:
            search_parts.append("author:" + author)
        if m_type and m_type != 'all':
            search_parts.append("type:" + m_type)
        if platform:
            search_parts.append("platform:" + platform)
        if arch:
            search_parts.append("arch:" + arch)
        if path:
            search_parts.append("path:" + path)
        if port:
            search_parts.append("port:" + port)
        if edb:
            search_parts.append("edb:" + edb)
        if bid:
            search_parts.append("bid:" + bid)
        if cve:
            search_parts.append("cve:" + cve)
        if reference:
            search_parts.append("reference:" + reference)
        if rank:
            search_parts.append("rank:" + rank)
        if check != 'None':
            search_parts.append("check:" + check)

        search_query = ' '.join(search_parts)
        if search_query == '':
            results = []
            return render_template('adv_search.html', toast=True, rows=results, filter_type=m_type)
        elif "type" not in search_query:
            results = client.modules.search(search_query)
            return render_template('adv_search.html', toast2=True, rows=results, filter_type=m_type)
        else:
            results = client.modules.search(search_query)
            return render_template('adv_search.html', rows=results, filter_type=m_type)
    else:
        return render_template('adv_search.html')

@index_bp.route('/module_details')
def module_details():
    module_type, module_name = request.args.get('module_type'), request.args.get('module_name')
    exploit = client.modules.use(module_type, module_name)
    return jsonify(exploit.info)
