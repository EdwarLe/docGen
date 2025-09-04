from flask import Blueprint, request, jsonify, send_file, current_app
from parsed import parse_python_code
from io import BytesIO

from exporter import generate_doc

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'] )
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    content = file.read().decode('utf-8', errors='replace')
    
    parse = parse_python_code(content)
    
    return parse

@main.route('/export', methods=['POST'] )
def export_file():
    
    # Force request to be json
    data = request.get_json(force=True)
    if not isinstance(data, list):
        return jsonify({
            "message": "Se esperaba una lista de bloques parseados",
            "status": 400
        }), 400
        
    title = data[0].get('title')
    
    # Generate word in memory
    doc = generate_doc(data, title=title)
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    
    # Return like download
    return send_file(
        buf,
        as_attachment=True,
        download_name=f"{title}.docx",
        mimetype=(
            "application/"
            "vnd.openxmlformats-"
            "officedocument.wordprocessingml.document"
        )
    )