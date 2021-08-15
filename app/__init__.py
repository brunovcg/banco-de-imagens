from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get('/download/<file_name>')
def download():
    ...

@app.get('/download-zip')
def download_dir_as_zip():
    ...


@app.get('/files')
def list_files():
    ...


@app.get('/files/<type>')
def list_files_by_type():
    ...

@app.get('/static/<path:filename>')
def static():
    ...

@app.post('/upload')
def upload():
    ...