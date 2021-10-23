import socket
import sys
import os
from types import CellType
import file_monitor
import tqdm
import shutil
import filecmp
    
path = sys.argv[1]
server_ip = "127.0.0.1" if sys.argv[2] == "localhost" else sys.argv[2]

def send_file(path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    # define port
    port = 10000
    buffer_size = 1024
    #server_ip = "127.0.0.1"
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
        print("\n")

def check_file_difference(path):
    # comparison directory
    comparison_dir = (os.getcwd()+"/server_version")
    similar = False
    for file in os.listdir(comparison_dir):
        file = os.path.join(comparison_dir, file)
        if filecmp.cmp(path, file, shallow=False)==True:
            print(f"file modified is similar to server's version of {os.path.basename(file)}")
            similar = True
            break
    if similar==False:
        send_file(path)

if __name__ == "__main__":
    # get path from argument and run watchdog monitor
    print(f"source directory: {path}, ip: {server_ip}")
    file_monitor.monitor_directory(path)