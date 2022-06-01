
from datetime import date, time, datetime
import sys, os
from pathlib import Path


import uuid


from smbprotocol.connection import Connection, Dialects



#from smbprotocol.connection import Connection, Dialects


userID = 'Administrator'
pw = '2292'
dir_name = 'PVDataLog\\'
server_name = '\\\pi\\'
share_name = 'd$\\'
file_name = '2022_03_07.CSV'
server_ip = '192.168.178.106'

s_path = server_name + share_name + dir_name

ip = server_ip

import subprocess
def ping_test (host):
	reached = []                           #Empty list to collect reachable host
	not_reached = []                          #Empty list to collect unreachable hosts
	for ip in host:
		ping_test = subprocess.call('ping %s -n 2' % ip)        #Ping host n times
		if ping_test == 0:                    #If ping test is 0, it' reachable
			reached.append(ip)
		else:
			not_reached.append(ip)                              #Else, it's not reachable

	print("{} is reachable".format(reached))
	print("{} not reachable".format(not_reached))

hosts = ["192.168.178.106", 'www.google.com',]         #Hosts list
ping_test (hosts)


#print(os.listdir("192.168.178.106"))

for i in os.environ:
	print(i)
#for entry in os.scandir(os.environ["LOCAL"]):
#	print(entry)


dir_file = s_path + file_name
print(s_path)
#print(dir_file)
#open(dir_file)

'''
with os.scandir(s_path) as ls:
	for item in ls:
		print(item)
				
'''		





#print(dir(smbprotocol))

'''


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

'''


