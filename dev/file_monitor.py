import socket
import os
import sys
from watchdog.observers import Observer
from watchdog.events import *
import time
import client

class Handler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            print(f"file modified:{event.src_path}")
            client.check_file_difference(event.src_path)
        

def monitor_directory(path):
    path_modified = ""
    # create directory for server version of iles
    if not os.path.exists(os.getcwd()+"/server_version"):
        os.makedirs(os.getcwd()+"/server_version")
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

