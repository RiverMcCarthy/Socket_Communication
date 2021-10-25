import socket
import sys
import io
import os
import time
import tqdm
import shutil

def start_server():
    # get destination directory path and ip address from command line argument
    path = sys.argv[1]
    ip = "127.0.0.1" if sys.argv[2] == "localhost" else sys.argv[2]
    # define socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # define the buffer size to be expected
    buffer_size = 1024
    print(f"destination directory: {path}, IP: {ip}")
    port = 10000
    server_socket.bind((ip, port))

    # queue up to five connections
    server_socket.listen(5)
    while True:
        # receive filename and filesize
        try:
            connection, address = server_socket.accept()
            bytes_received = connection.recv(buffer_size).decode()

            # split string by "<>" to get filename and filesize
            filename, filesize = bytes_received.split("<>")
            filesize = int(filesize)
            with tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=buffer_size) as progress:
                with open(path+"/"+filename, "wb") as f:
                    while True:
                        # read 1024 bytes from the socket
                        bytes_read = connection.recv(buffer_size)
                        if not bytes_read:    
                            # file has been received
                            break

                        # write to file
                        f.write(bytes_read)

                        # update the progress bar
                        progress.update(len(bytes_read))
                    f.close
        except Exception as e:
            # print error details for debugging
            print(f"error: {e}")
            # close socket connection
            server_socket.close

    # close socket connection
    server_socket.close
    

if __name__ == '__main__' :
    start_server()