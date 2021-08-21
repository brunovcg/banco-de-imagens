from kenzie import formats, max_size


def is_smaller_than_Authorized(file_size:int):
    """Receives a file size and check if it's size is equal or less then
    what was parametrized on .env.

    Args: 
        file_size (int): Integer to be compared with the setted size.

    Returns:
        boolean: Returns true if it is smaller or equal and false if not.  
    """
    import re
    converted_max_size = int(re.sub('[^0-9]', '', max_size))

    if file_size <= converted_max_size * 1000 * 1000:
        return True
    return False


def is_supported_format(file_format:str):
    """Receives a file format and check if it's included on the list on .env.

    Args: 
        file_formart (str): Integer to be compared with the supported types of files.

    Returns:
        boolean: Returns true if it is supportable and false if not. 
    """
    if file_format in formats:
        return True
    return False


def list_all_files():
    """Get all file names that are in the folders database.
    
    Returns:
        list: Returns a list with all the file names.
    """

    import os
    all_files = []
    folders_in_storage = os.listdir('kenzie/storage')
    for folder in folders_in_storage:
        folder_files = os.listdir(f'kenzie/storage/{folder}')
        all_files += folder_files
    return all_files


def list_all_file_with_specific_format(format: str):
    """Get all file names with a specific type that are in the folders database.
    
    Args: 
        format (str): A string to be checked if it is included on database.

    Returns:
        list: Returns a list with the file names that match the condition mentioned.
    """

    all_list = list_all_files()

    filtered_formats = [item for item in all_list if format in item]
    
    return filtered_formats


def file_name_does_exist(file_name: str):
    """Check if an specific file exists on database.
    
    Args: 
        file_name (str): A string to checked if the file exists on database.

    Returns:
        boolean: Returns true if exists and false with not.
    """
   
    if file_name in list_all_files():
        return True
    return False


def compress_file(type : str, rate : str):
    """Function that allows to download files in a zip folder using flask.
    
    Args: 
        type (str): The file type to be downloaded on flask, if the request won't use it, just write a empty string "".
        rate (str): The compress_rate for the file, if the request in flask won't use it, just write a empty string "".

    Returns:
        void : It wont return anything, it creates a zip folder on PC tmp folder and then downloads with flask.
    """

    import os

    default_rate = "1"

    if rate != "":
        default_rate = rate

    if type != "":
        os.system(f"cd kenzie/storage/ && zip -{default_rate} /tmp/image.zip ./{type}/* && cd -")
    else:
         os.system(f"cd kenzie/storage && zip -{default_rate} /tmp/image.zip ./*/* && cd -")
