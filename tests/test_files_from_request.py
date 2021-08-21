from app import app
from kenzie.image import list_all_file_with_specific_format, list_all_files
from kenzie import formats
import os

test_client = app.test_client()

main_diretory = "kenzie/storage/"

    
# tests for /files/<type>  _______________________________________________________

def test_if_filestype_show_error_if_a_file_type_that_is_not_in_database():

    assert test_client.get('/files/bin').status_code == 404


def test_if_show_a_filetype_if_it_exists_otherwise_show_error():

    filetype = "png"

    files_of_this_type = list_all_file_with_specific_format(filetype)

    if len(files_of_this_type) > 1:
        assert test_client.get(f'/files/{filetype}').status_code == 200
        assert test_client.get(f'/files/{filetype}').get_json() == files_of_this_type
    else:
        assert test_client.get(f'/files/{filetype}').status_code == 404


# tests for /download-zip    _______________________________________________________

def test_error_for_download_zip_if_there_are_no_files_or_not():

    files = list_all_files()

    if len(files) < 1:
        assert test_client.get('/download-zip').status_code == 404
    else:
        assert test_client.get('/download-zip').status_code == 200


def test_error_for_download_zip_if_it_works_with_parameters():


    files = list_all_files()

    if len(files) < 1:
        assert test_client.get('/download-zip?compression_rate=1&file_type=jpg').status_code == 404
    else:
        assert test_client.get('/download-zip?compression_rate=1&file_type=jpg').status_code == 200
          
def test_check_if_file_downloaded_is_zip():

    files = list_all_files()

    if len(files) > 0:
        assert test_client.get('/download-zip?compression_rate=1&file_type=jpg').headers.get("Content-Type") == "application/zip"
    else:
        assert test_client.get('/download-zip?compression_rate=1&file_type=jpg').status_code == 404


# tests for /download/<file_name>     _______________________________________________________

def test_error_for_download_the_file_exists_in_database():

    files = list_all_files()

    if "kenzie.png" not in files:
        assert test_client.get('/download/kenzie.png').status_code == 404
    else:
        assert test_client.get('/download/kenzie.png').status_code == 200


def test_if_the_file_format_downloaded_has_the_same_extention_as_asked():

    
    files = list_all_files()

    if "kenzie.jpg" not in files:
        assert test_client.get('/download/kenzie.jpg').status_code == 404
    else:
        assert test_client.get('/download/kenzie.jpg').headers.get("Content-Type") == "image/jpeg"


def test_if_download_allows_get_method():
   assert 'GET' in (test_client.options('/download/kenzie.png').headers['Allow'])



# tests for /upload     _______________________________________________________


def test_error_in_upload_because_of_extension_type():
    from werkzeug.datastructures import FileStorage

    folders = os.listdir('tests')
    testfolder = os.listdir('tests/testsfiles')
    file_test = "kenzie.txt"

    if "testsfiles" not in folders:
        
        os.system("mkdir tests/testsfiles")
        os.system(f"touch tests/testsfiles/{file_test}")

    elif "testsfiles" in folders and file_test not in testfolder:
        os.system(f"touch tests/testsfiles/{file_test}")


    file_path = './tests/testsfiles/kenzie.txt'
    with open(file_path, 'rb') as file:
        my_file = FileStorage(stream=file, filename='kenzie.txt', content_type='text/plain', content_length="50")

        response = test_client.post('/upload', data={"file": my_file}, content_type="multipart/form-data", content_length="50")

        assert response.status_code == 415


def test_error_in_upload_because_already_exists():
    from werkzeug.datastructures import FileStorage

    folders = os.listdir('tests')
    testfolder = os.listdir('tests/testsfiles')
    file_test = "kenzie.png"

    if "testsfiles" not in folders:
        
        os.system("mkdir tests/testsfiles")
        os.system(f"touch tests/testsfiles/{file_test}")

    elif "testsfiles" in folders and file_test not in testfolder:
        os.system(f"touch tests/testsfiles/{file_test}")


    file_path = './tests/testsfiles/kenzie.png'
    with open(file_path, 'rb') as file:
        my_file = FileStorage(stream=file, filename='kenzie.png', content_type='image/png', content_length="5000")

        response = test_client.post('/upload', data={"file": my_file}, content_type="multipart/form-data", content_length="5000")

        files = list_all_files()

        if file_test in files:

            assert response.status_code == 409

# tests for /files _______________________________________________________


def test_if_files_allows_get_method():
    assert 'GET' in (test_client.options('/files').headers['Allow'])
    

def test_files_status_codes_if_the_folders_have_files_or_not():
    
    files = list_all_files()

    if len(files) < 1:
        assert test_client.get('/files').status_code == 404
    else:
        assert test_client.get('/files').status_code == 200
        assert test_client.get('/files').get_json() == files
