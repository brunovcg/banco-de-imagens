from flask import Flask, request, jsonify, safe_join, send_from_directory
from werkzeug.utils import secure_filename
from kenzie.image import (is_supported_format,
                            file_name_does_exist,
                            is_smaller_than_Authorized, 
                            list_all_file_with_specific_format,
                            max_size, 
                            list_all_files,
                            compress_file                      
                            )
                            
from kenzie.__init__ import formats, create_folder_structure

app = Flask(__name__)


try:
    create_folder_structure()
except FileExistsError:
    ...


@app.get('/download/<file_name>')
def download(file_name):
 

    if not file_name or not file_name in list_all_files():
        return {"message" : f"Error - The file '{file_name}' does not exist on database"}, 404

    file_format = file_name.split('.')[-1]
    
    return send_from_directory(directory=f"../kenzie/storage/{file_format}", path=f"{file_name}", as_attachment=True), 200


@app.get('/download-zip')
def download_dir_as_zip():


    if len(list_all_files()) == 0:
        return {"message" : "Error - Database has no files"},404
    
    file_type = request.args.get("file_type")

    compression_rate = request.args.get("compression_rate")

    if not file_type:
        file_type = ""

    if not compression_rate:
        compression_rate = ""
        
    compress_file(file_type,compression_rate)
  
    return send_from_directory(directory="/tmp/", path="image.zip", as_attachment=True), 200
  

@app.get('/files')
def list_files():

    files = list_all_files()

    if len(files) < 1:
        return {"message" : "Error - The are no files on our database"}, 404 

    return jsonify(files), 200


@app.get('/files/<type>')
def list_files_by_type(type):


    filtered = list_all_file_with_specific_format(type)

    if len(filtered) < 1:
        return {"message" : f"Error - There is no file with '{type}' format"}, 404

    return jsonify(filtered), 200


@app.post('/upload')
def upload():
   
    try:
        file = request.files["file"]

    except KeyError:
        return {"message" : "Error - You didn't attached a file with name 'file' "}, 406
    
    file_name = secure_filename(file.filename)

    file_format = file_name.split('.')[-1]

    file_size = request.headers.get("Content-Length", 0)
   
      
    if not is_supported_format(file_format):
        return {"message" : f"Error - The only supported file extentions are: '{', '.join(formats)}'. You tried a '{file_format}' file"}, 415
  

    if file_name_does_exist(file_name):
        return {"message" : f"Error - A file with named '{file_name}' already exists on our database, upload this file with another name"}, 409

    if not is_smaller_than_Authorized(int(file_size)):
        return {"message": f"Error - This file is bigger than {max_size}"}, 413
   
    upload_directory = f"./kenzie/storage/{file_format}"

    file_path = safe_join(upload_directory, file_name)

    file.save(file_path)

    return {"message" : f"File '{file_name}' was uploaded"}, 201
