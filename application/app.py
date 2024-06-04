# app.py
from flask import Flask
from routes.scan_result import scanres
from routes.scan import scan
from routes.index import index_bp  
from routes.exploit import exploit_bp

app = Flask(__name__)
app.register_blueprint(scanres, url_prefix='/scan-results')
app.register_blueprint(scan, url_prefix='/scan')
app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(exploit_bp, url_prefix='/exploit')


if __name__ == "__main__":
    app.run(debug=True)
