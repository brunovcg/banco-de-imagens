from environs import Env
from os import environ
import os

env = Env()

folder = environ.get("FILES_DIRECTORY")

active_in_folder= os.listdir(folder)


formats = ['png', 'jpg','gif']

if not "storage" in active_in_folder:
    os.mkdir("kenzie/storage")

else:
    active_in_storage = os.listdir('kenzie/storage')
    for item in formats:
        if not item in active_in_storage:
            os.mkdir(f"kenzie/storage/{item}")
            

