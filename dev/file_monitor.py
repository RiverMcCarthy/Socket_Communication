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
    # if a file is modified then compare files
    def on_modified(self, event):
        # ignore directory modifications
        if event.is_directory:
            pass
        else:
            print(f"file modified:{event.src_path}")
            client.compare_files(event.src_path)
        

def monitor_directory(path):
    # create directory for server version of iles
    if not os.path.exists(os.getcwd()+"/server_version"):
        os.makedirs(os.getcwd()+"/server_version")
    observer = Observer()
    # run handler
    event_handler = Handler()
    # monitor directory tree
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    # monitor once every second
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

