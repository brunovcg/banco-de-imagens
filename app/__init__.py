from flask import Flask, request, jsonify
from kenzie import folder, active_in_folder

app = Flask(__name__)


@app.get('/download/<file_name>')
def download():
    return 'teste'


@app.get('/download-zip')
def download_dir_as_zip():
    return "teste2"


@app.get('/files')
def list_files():
    return'teste'


@app.get('/files/<type>')
def list_files_by_type():
    return "teste4"


# @app.get('/static/<path:filename>')
# def static():
#     return "teste5"


@app.post('/upload')
def upload():
    return "teste6"