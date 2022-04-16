
from datetime import date, time, datetime
import os
from pathlib import Path

import uuid

from smbprotocol.connection import Connection, Dialects
import smbclient

from smbclient import (
    link,
    open_file,
    remove,
    register_session,
    stat,
    symlink,
    rename,
)

from smbclient import (
    listdir,
    mkdir,
    register_session,
    rmdir,
    scandir,
)

from smbclient.path import (
    isdir,
)




userID = 'Administrator'
pw = '2292'
dir_name = '\\PVDataLog'
server_name = 'pi'
share_name = '\\\pi\d$'
server_ip = '192.168.178.106'

dir_log_data  = share_name + dir_name


dir = share_name + dir_name + '\\xxx'

dir_file = share_name + dir_name + '\\2022_03_07.CSV'

print(dir_log_data)
print(dir)
print(dir_file)



'''
smbclient.register_session(server_name, username=userID, password=pw)


#connection = Connection(uuid.uuid4(), server_name, 445)
#connection.connect(Dialects.SMB_3_0_2)
#print(dir(connection))

#smbclient.ClientConfig(username=userID, password=pw)



#smbclient.mkdir(dir, username=userID, password=pw)


#with smbclient.open_file(dir_file, mode="r") as fd:
 #  a = fd.read()
   
   
#print(a)


# Use scandir as a more efficient directory listing as it already contains info like stat and attributes.
for file_info in scandir(dir_log_data):
    file_inode = file_info.inode()
    if file_info.is_file():
        print("File: %s %d" % (file_info.name, file_inode))
    elif file_info.is_dir():
        print("Dir: %s %d" % (file_info.name, file_inode))
    else:
        print("Symlink: %s %d" % (file_info.name, file_inode))

'''

print('-----')

#a = GetNWCSV_File_Names(dir_log_data, server_name, userID, pw)
#print(a.fileNamesSizeTublesArray)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#print(ROOT_DIR)


ROOT_DIR = os.path.abspath(os.curdir)

#print(ROOT_DIR)



#defining a function to find index in a list using lambda
get_indexes = lambda x, searchable: [i for (y, i) in zip(searchable, range(len(searchable))) if x == y]

p = str(Path(__file__).parents[0])
p_list = p.split("/")
index_1 = len(p_list)
index_2 = get_indexes('Repositories', p_list)[0]
root_index = index_1 - index_2 - 2
root = str(Path(__file__).parents[root_index])
print(root)
print('-.-.-.-')


print('---')




