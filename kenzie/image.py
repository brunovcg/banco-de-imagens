import os
import re
from kenzie import formats, max_size


def smaller_than_Authorized(file_size):
    
    converted_max_size = int(re.sub('[^0-9]', '', max_size))

    if file_size <= converted_max_size * 1000 * 1000:
        return True
    return False


def is_acceptable_format(file_format):
    if file_format in formats:
        return True
    return False

def file_name_does_exist(file_name):

    all_files = []
    folders_in_storage = os.listdir('kenzie/storage')
    for folder in folders_in_storage:
        folder_files = os.listdir(f'kenzie/storage/{folder}')
        all_files += folder_files

    if file_name in all_files:
        return True
    return False



def download_all_files_zip():
    ...

def download_all_file_with_specific_format():
    ...


