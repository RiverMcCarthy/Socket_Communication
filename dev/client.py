import socket
import sys
import os
import file_monitor
import tqdm
import shutil
    
# get source directory path and ip address from command line argument
path = sys.argv[1]
server_ip = "127.0.0.1" if sys.argv[2] == "localhost" else sys.argv[2]
sim_thresh = float(sys.argv[3])

def send_file(path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    # define port
    port = 10000
    # set buffer size
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
    # number of lines in modified file which are also in 
    same = 0
    num_lines = 0
    # iterate through comparison files of same name and compare contents
    for name_comp in os.listdir(comparison_dir):
        if name_comp == os.path.basename(path_mod):
            path_comp = os.path.join(comparison_dir, name_comp)
            # read text of modified and comparison files
            with open(path_mod, "r", errors='replace') as file_mod, open(path_comp, "r", errors='replace') as file_comp:
                # compare lines of modified file with comparison file contents
                lines_mod = file_mod.readlines()
                num_lines = len(lines_mod)
                lines_comp = file_comp.readlines()
                for line_mod in lines_mod:
                    if line_mod in lines_comp:
                        same+=1
                file_mod.close
                file_comp.close
    # if there is contents to the file
    if (num_lines)>0:
        similarity = 100*same/(num_lines)
    else:
        similarity = 0
    # check if the similarity is less than the threshold
    if similarity<sim_thresh:
        send_file(path_mod)
    else:
        print(f"file is similar to backed up version")


if __name__ == "__main__":
    # get path from argument and run watchdog monitor
    print(f"source directory: {path}, ip: {server_ip}, similarity threshold: {sim_thresh}")
    file_monitor.monitor_directory(path)