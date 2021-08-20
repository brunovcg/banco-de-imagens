from threading import stack_size
from flask import Flask, request, jsonify, safe_join
from werkzeug.utils import secure_filename


app = Flask(__name__)


from kenzie.image import is_acceptable_format, file_name_does_exist, smaller_than_Authorized, max_size


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




@app.post('/upload')
def upload():

    try:
        file = request.files["file"]

    except KeyError:
        return {"message" : "You didn't attached a file with name 'file' "}, 406
    

    file_name = secure_filename(file.filename)

    file_format = file_name.split('.')[-1]

    file_size = request.headers.get("Content-Length", 0)
   
    if not smaller_than_Authorized(int(file_size)):
        return {"message": f"This file is bigger than {max_size}"}, 413

    
    if not is_acceptable_format(file_format):
        return {"message" : f"The only supported file extentions are: 'png','jpg' and 'gif', you tried a '{file_format}' file"}, 415

    if file_name_does_exist(file_name):
        return {"message" : f"A file with a same name is saved on our database, upload this file with another name"}, 409

   
    upload_directory = f"./kenzie/storage/{file_format}"

    file_path = safe_join(upload_directory, file_name)

    file.save(file_path)











    return jsonify(f"File '{file_name}' was uploaded"), 201


