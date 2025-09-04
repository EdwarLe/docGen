from flask import Blueprint, request

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'] )
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    content = file.read().decode('utf-8', errors='replace')
    print(content)
    return 'Hello World!'