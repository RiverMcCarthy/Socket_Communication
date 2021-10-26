# Server-Client File Backup using Socket Communication

## Introduction 
The aim of this project is to create a programme designed to back up file modifications to a remote (or local) server. The estimated time devoted to this project is around 4-5 hours.

client side interface example
![image](./image1.png)
server side interface example
![image](./image2.png)

## Getting Started
Install the below dependencies to run the projects on a local device
1. Dependencies
    * [Python](https://www.python.org/downloads/)
    * socket
    * [tqdm](https://github.com/tqdm/tqdm)
    * [shutil](https://docs.python.org/3/library/shutil.html)
    * [watchdog](https://pypi.org/project/watchdog/)
2. Essential Logic
    * The client runs a file monitor script to check for any changes to files in the source directory. The filename and filesize is then sent to the server and then the file is sent and saved to the specified destination directory. A local (client side) directory called [server_version](./server_version) is created and a copy of the file is saved and used for future reference to check if file modifications are different to the server version. This prevents redundant file backup to the server and allows the client to check which version is in the server's destination directory. Originally filecomp.cmp library was used to compare files but this was seen to be ineffective. Comparing the binary files was also assumed to be ineffective as the difference in bytes is not necessarily correlated to the text difference. The files were therefore compared by directly equating lines. For each line of the modified file, the exact matches with any line in server version of the same filename are added up and if the percentage of matched lines out of total lines of the modified file is less than a threshold then the file is send to the server. i.e. threshold of 100 means for any change the file will be sent to server, whereas a threshold of 50 would mean that if more than half the lines of the modified file are not in the server version of the file then the file will be sent to the server.

## Build and Test
1. Open a new terminal and set up the server

Navigate to repository directory and run [server.py](./dev/server.py) where DESTINATION_DIR is the desired destination directory and IP is the server IP address.

``` $ cd Socket_Communication ```

``` $ python3 dev/server.py DESTINATION_DIR IP``` for MacOS or ``` $ python dev/server.py DESTINATION_DIR IP``` for Windows or Linux


2. Open a second terminal and set up the client

Navigate to repository directory and run [client.py](./dev/client.py) where SOURCE_DIR is the desired source directory, IP is the server IP address, and SIMILARITY_THRESHOLD is the percentage of similarity to allow for. If SIMILARITY_THRESHOLD is 100 then for any modification the file will be sent to the server.

``` $ cd Socket_Communication ```

``` $ python3 dev/client.py SOURCE_DIR IP SIMILARITY_THRESHOLD```

3. For local testing a source and destination repository have been created and localhost ("127.0.0.1") can be used by entering

``` $ python3 dev/server.py data/dest localhost```
in a new terminal

and then

``` $ python3 dev/client.py data/source localhost 100```
in another terminal.

4. Modify [test.txt](./data/source/test.txt) to test programme operation.

5. Alter the similarity threshold to preference

## Scripts
### Python Files
* [server.py](./dev/server.py) sets up the server
* [client.py](./dev/client.py) initiates file backup
* [file_monitor.py](./dev/file_monitor.py) monitors files in the specified directory


## To Do
* Optimise file comparison to adjust similarity threshold
* The file comparison currently only compares lines to check for file duplication but the criteria could be modified to fit the use case of the application.
* Add optional features to allow force backup requests
