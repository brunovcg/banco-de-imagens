import os
import re
from kenzie import formats, max_size


def is_smaller_than_Authorized(file_size):
    
    converted_max_size = int(re.sub('[^0-9]', '', max_size))

    if file_size <= converted_max_size * 1000 * 1000:
        return True
    return False


def is_supported_format(file_format):
    if file_format in formats:
        return True
    return False



def list_all_files():
    all_files = []
    folders_in_storage = os.listdir('kenzie/storage')
    for folder in folders_in_storage:
        folder_files = os.listdir(f'kenzie/storage/{folder}')
        all_files += folder_files
    return all_files


def list_all_file_with_specific_format(format):

    all_list = list_all_files()

    filtered_formats = [item for item in all_list if format in item]
    
    return filtered_formats



def file_name_does_exist(file_name):
   
    if file_name in list_all_files():
        return True
    return False

