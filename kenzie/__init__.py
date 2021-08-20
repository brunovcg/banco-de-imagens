from environs import Env
from os import environ
import os

env = Env()

main_path = environ.get("FILES_DIRECTORY")

folders_in_storage= os.listdir(main_path)


formats = ['png', 'jpg','gif']

if not "storage" in folders_in_storage:
    os.mkdir("kenzie/storage")

else:
    active_in_storage = os.listdir('kenzie/storage')
    for item in formats:
        if not item in active_in_storage:
            os.mkdir(f"kenzie/storage/{item}")
            

