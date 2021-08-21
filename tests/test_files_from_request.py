from app import app
from kenzie.image import list_all_files
from kenzie import formats
import os

test_client = app.test_client()

main_diretory = "kenzie/storage/"

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

    
# tests for /files/<type>  _______________________________________________________

def test_if_filestype_show_error_if_a_file_is_not_in_database():

    assert test_client.get('/files/bin').status_code == 404


# tests for /download-zip    _______________________________________________________

def test_error_if_the_are_no_files():

    files = list_all_files()

    if len(files) < 1:
        assert test_client.get('/download-zip').status_code == 404
    else:
        assert test_client.get('/download-zip').status_code == 200
 
    
# tests for /download/<file_name>     _______________________________________________________

def test_error_for_download_the_file_exists_in_database():

    files = list_all_files()

    if "kenzie.png" not in files:
        assert test_client.get('/download/kenzie.png').status_code == 404
    else:
        assert test_client.get('/download/kenzie.png').status_code == 200





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


    FILE_PATH = './tests/testsfiles/kenzie.txt'
    with open(FILE_PATH, 'rb') as file:
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


    FILE_PATH = './tests/testsfiles/kenzie.png'
    with open(FILE_PATH, 'rb') as file:
        my_file = FileStorage(stream=file, filename='kenzie.png', content_type='image/png', content_length="5000")

        response = test_client.post('/upload', data={"file": my_file}, content_type="multipart/form-data", content_length="5000")

        files = list_all_files()

        if file_test in files:

            assert response.status_code == 409
    
   










