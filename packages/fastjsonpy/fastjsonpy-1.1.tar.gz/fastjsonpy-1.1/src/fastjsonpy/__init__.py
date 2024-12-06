import json
from threading import Thread
import time

files = {}

def init(file):
    global files
    if not file in files.keys():
        files[file] = json.load(open(file, 'r'))
        Thread(target=updatefile_thread, args=(file,)).start()
    else:
        raise Exception('File already opened')

def updatefile_thread(file):
    global files
    while True:
        with open(file, 'w') as f:
            json.dump(files[file], f)
        time.sleep(5)

def get(file):
    global files
    if file in files.keys():
        return files[file]
    else:
        raise Exception('File not opened')

def set(file, data):
    global files
    if file in files.keys():
        files[file] = data
    else:
        raise Exception('File not opened')

def updatefile(file):
    if file in files.keys():
        with open(file, 'w') as f:
            json.dump(files[file], f)
    else:
        raise Exception('File not opened')
