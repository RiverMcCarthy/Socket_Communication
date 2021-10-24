import socket
import sys
import os
from types import CellType
import file_monitor
import tqdm
import shutil
from difflib import SequenceMatcher
    
path = sys.argv[1]
server_ip = "127.0.0.1" if sys.argv[2] == "localhost" else sys.argv[2]

def send_file(path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    # define port
    port = 10000
    buffer_size = 1024
    client_socket = socket.socket()
    client_socket.connect((server_ip, port))
    # send filename and filesize
    try:
        client_socket.send(f"{filename}<>{filesize}".encode())
        # start sending the file
        with tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024) as progress:
            with open(path, "rb") as f:
                while True:

                    # read bytes from file
                    bytes_read = f.read(buffer_size)

                    if not bytes_read:
                        # file sent
                        break
                    client_socket.sendall(bytes_read)
                    # update progress bar
                    progress.update(len(bytes_read))
            shutil.copyfile(path, os.getcwd()+f"/server_version/{filename}")
    finally:
        # close the socket
        client_socket.close()
        f.close
        print("\n")

def compare_files(path_mod):
    # comparison directory
    comparison_dir = (os.getcwd()+"/server_version")
    similar = False
    # iterate through comparison files of same name and compare contents
    for name_comp in os.listdir(comparison_dir):
        if name_comp == os.path.basename(path_mod):
            path_comp = os.path.join(comparison_dir, name_comp)
            # read text of modified and comparison files
            with open(path_mod, "r", errors='replace') as file_mod, open(path_comp, "r", errors='replace') as file_comp:
                for line_mod in file_mod.readlines():
                    for line_comp in file_comp.readlines():
                        if line_comp == line_mod:
                            print(f"file is similar to backed up version")
                            similar = True
                            file_mod.close
                            file_comp.close
                            break
    # send file to server if no lines of modified file are the same as lines of comparison file
    if similar==False:
        send_file(path_mod)


if __name__ == "__main__":
    # get path from argument and run watchdog monitor
    print(f"source directory: {path}, ip: {server_ip}")
    file_monitor.monitor_directory(path)