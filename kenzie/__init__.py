from environs import Env
from os import environ
import os

env = Env()

main_path = environ.get("FILES_DIRECTORY")
formats = ["png","jpg","gif"]
max_size = environ.get("MAX_CONTENT_LENGTH")


def create_folder_structure():

    folders_in_storage= os.listdir(main_path)

    if not "storage" in folders_in_storage:
        os.mkdir("kenzie/storage")
        for item in formats:
            os.mkdir(f"kenzie/storage/{item}")              
            