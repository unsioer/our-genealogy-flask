from flask import Blueprint, request, jsonify, send_from_directory
import time
import os
from flask_jwt_extended import (
    jwt_required
)
import json
import settings
import base64

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

@file_bp.route('/file/json', methods=['POST'])
#@jwt_required()
def upload_json():
    data = json.loads(request.get_data())
    filename= data['filename']
    base = data['content']
    byte=base64.b64decode(base)
    print(byte)
    filename=str(int(time.time()))+filename
    with open(os.path.join(settings.STATIC_ROOT, filename),'wb') as f:
        f.write(byte)
        return jsonify({'msg':'200','filename':filename})
    '''if file.filename == '':
        return jsonify({'msg': 'No selected file'})
    if file:
        filename = str(int(time.time()))+file.filename
        file.save(os.path.join(settings.STATIC_ROOT, filename))
        return jsonify({'msg':'200','filename':filename})
'''
    return jsonify({'msg':'Unknown'})

@file_bp.route('/file/<string:filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(settings.STATIC_ROOT, filename)
    except Exception as e:
        return str(e)