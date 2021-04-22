from flask import Blueprint, request, jsonify, send_from_directory
import time
import os
from flask_jwt_extended import (
    jwt_required
)
import settings

file_bp = Blueprint("file", __name__)


@file_bp.route('/file', methods=['POST'])
@jwt_required()
def upload():
    print(request)
    if 'file' not in request.files:
        return jsonify({'msg':'no file'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'msg': 'No selected file'})
    if file:
        filename = str(int(time.time()))+file.filename
        file.save(os.path.join(settings.STATIC_ROOT, filename))
        return jsonify({'msg':'200','filename':filename})

    return jsonify({'msg':'Unknown'})

@file_bp.route('/file/<string:filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(settings.STATIC_ROOT, filename)
    except Exception as e:
        return str(e)