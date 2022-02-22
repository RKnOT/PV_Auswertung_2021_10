# -*- coding: utf-8 -*-
# based   on   https://github.com/humberry/smb-example/blob/master/smb-test.py
# smb+nmb from https://github.com/miketeo/pysmb/tree/master/python3
# pyasn1  from https://github.com/etingof/pyasn1
from io import BytesIO
from smb.SMBConnection import SMBConnection
from smb import smb_structs
from nmb.NetBIOS import NetBIOS
import os
import sys
from socket import gethostname
from io import StringIO

class SMB_client():
	def __init__(self,username=None,password=None,smb_name=None,print_errors=True):
		self.username     = username
		self.password     = password
		self.smb_name     = smb_name
		self.print_errors = print_errors
		self.smb_ip       = None
		self.conn         = None
		self.service_name = None
		self.my_name      = None
		self.error        = None
		self.tree         = []

	def getBIOSName(self, remote_smb_ip, timeout=5):			# unused if dynamic IP
		# ip -> smb name
		try:
			self.error = None
			bios = NetBIOS()
			srv_name = bios.queryIPForName(remote_smb_ip, timeout=timeout)
			return srv_name[0]
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
			return None
			
	def getIP(self):
		# smb name -> ip
		try:
			self.error = None
			bios = NetBIOS()
			ip = bios.queryName(self.smb_name)
			return ip[0]
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
			return None
			
	def connect(self):
		try:
			self.error = None
			self.my_name = 'pi'			# iDevice name
			#self.smb_ip = self.getIP()
			#print(self.smb_ip)
			self.smb_ip = socket.gethostbyname(server_name)
			print(self.smb_ip)
			smb_structs.SUPPORT_SMB2 = True
			
			#conn = SMBConnection(userID, password, client_machine_name, server_name, use_ntlm_v2 = True)""
			self.conn = SMBConnection(self.username, self.password, self.my_name, self.smb_name, use_ntlm_v2 = True)
			print(dir(self.conn))
			self.conn.connect('pi', 445)		#139=NetBIOS / 445=TCP
			if self.conn:
				shares = self.conn.listShares()
				for share in shares:
					if share.type == 0:		# 0 = DISK_TREE
						self.service_name = share.name  
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
			
	def close(self):
		try:
			self.error = None
			self.conn.close()
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
 
	def getRemoteDir(self, path, pattern):
		try:
			self.error = None
			files = self.conn.listPath(self.service_name, path, pattern=pattern)
			return files
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
			return None
				
	def getRemoteTree(self,path=''):
		try:
			self.error = None
			if path == '':
				w = ''
			else:
				w = path+'/'
			files = self.getRemoteDir(path, '*')
			if files:
				for file in files:
					if file.filename[0] == '.':
						continue
					self.tree.append({'name':w+file.filename, 'isdir':file.isDirectory, 'size':file.file_size})
					if file.isDirectory:
						self.getRemoteTree(path=w+file.filename)
			return self.tree
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
			return None

	def download(self, path, filename,buffersize=None,callback=None, local_path=None):
		try:
			self.error = None
			#print('Download = ' + path + filename)
			attr = self.conn.getAttributes(self.service_name, path+filename)
			#print('Size = %.1f kB' % (attr.file_size / 1024.0))
			#print('start download')
			file_obj = BytesIO()
			if local_path:
				fw = open(local_path+filename, 'wb')
			else:
				fw = open(filename, 'wb')
			offset = 0
			transmit =0
			while True:
				if not buffersize:
					file_attributes, filesize = self.conn.retrieveFile(self.service_name, path+filename, file_obj)
				else:
					file_attributes, filesize = self.conn.retrieveFileFromOffset(self.service_name, path+filename, file_obj,offset=offset,max_length=buffersize)
					if callback:
						transmit = transmit + filesize
						callback(transmit)
				file_obj.seek(offset)
				for line in file_obj:
					fw.write(line)
				offset = offset + filesize
				if (not buffersize) or (filesize == 0):
					break
			fw.close()
			#print('download finished')
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
			
	def upload(self, path, filename,buffersize=None,callback=None, local_path=None):
		try:
			self.error = None
			#print('Upload = ' + path + filename)
			#print('Size = %.1f kB' % (os.path.getsize(filename) / 1024.0))
			#print('start upload')
			if local_path:
				file_obj = open(local_path+filename, 'rb')
			else:
				file_obj = open(filename, 'rb')
			offset = 0
			while True:
				if not buffersize:
					filesize = self.conn.storeFile(self.service_name, path+filename, file_obj)
					break
				else:	
					buffer_obj = file_obj.read(buffersize)			
					if buffer_obj:
						buffer_fileobj = BytesIO()
						buffer_fileobj.write(buffer_obj)
						buffer_fileobj.seek(0)
						offset_new = self.conn.storeFileFromOffset(self.service_name, path+filename, buffer_fileobj, offset=offset, truncate=False)
						#return the file position where the next byte will be written.
						offset = offset_new
						if callback:
							callback(offset)
					else:
						break
			file_obj.close()
			#print('upload finished')
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)

	def delete_remote_file(self,path, filename):
		try:
			self.error = None
			self.conn.deleteFiles(self.service_name, path+filename)
			#print('Remotefile ' + path + filename + ' deleted')
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)

	def createRemoteDir(self, path):
		try:
			self.error = None
			self.conn.createDirectory(self.service_name, path)
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)
  
	def removeRemoteDir(self,path):
		try:
			self.error = None
			self.conn.deleteDirectory(self.service_name, path)
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)

	def renameRemoteFileOrDir(self,old_path, new_path):
		try:
			self.error = None
			self.conn.rename(self.service_name, old_path, new_path)
		except Exception as e:
			if self.print_errors:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
			else:
				self.error = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e)

#-----------------

import socket
import os
import paramiko

import urllib
import smb
from smb.SMBHandler import SMBHandler

from smb.SMBConnection import SMBConnection
################


userID = 'Administrator'
pw = '2292'
dir_name = 'PVDataLog'
server_name = 'pi'
share_name = '\\pi\d$'
server_ip = '192.168.178.106'


print(socket.gethostbyname(server_name))
print(socket.gethostbyaddr(server_ip))
print(gethostname())	

#print(socket.gethostbyname(server_name))
#print(socket.gethostbyaddr(server_ip))
#print(gethostname())

#director = urllib.request.build_opener(SMBHandler)
#fh = director.open('smb://Admimistrator:2292@192.168.178.106/\\pi\d$\PVDataLog')
# Process fh like a file-like object and then close it.
#fh.close()

# For paths/files with unicode characters, simply pass in the URL as an unicode string
#fh2 = director.open(u'smb://myuserID:mypassword@192.168.1.1/sharedfolder/测试文件夹/垃圾文件.dat')

# Process fh2 like a file-like object and then close it.


dir = share_name +'\\'+ dir_name
#print(dir)


#smb = SMB_client(username=userID, password=pw, smb_name=server_name)

#smb.getIP()
#smb.connect()
#tree_all = smb.getRemoteTree()
#print(tree_all)





#command ='ls'
#command ='listdir'
#client = paramiko.SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect(hostname=server_name, username=userID, password=pw)

#v_sftp = client.open_sftp()

#v_sftp.chdir(dir)
#for loop in v_sftp.listdir():
 #   rmt_dirs.append(loop)


#stdin, stdout, stderr = client.exec_command('df ; free')
#stdin,stdout,stderr= client.exec_command(command)
#print(stdout.read())
#print(stderr.readlines)
#print(stderr)
#print 'SSH connection established with ' + strComputer + ' as user ' + strUser + '.'




#smb = smbclient.SambaClient(server= server_name, share=dir_name, username=userID, password=pw, domain='baz')
#print(smb.volume)
#print(smb.diskinfo())
#print(smb.listdir('/'))

# There will be some mechanism to capture userID, password, client_machine_name, server_name and server_ip
# client_machine_name can be an arbitary ASCII string
# server_name should match the remote machine name, or else the connection will be rejected
#conn = SMBConnection(userID, password, client_machine_name, server_name, use_ntlm_v2 = True)
#assert conn.connect(server_ip, 139)

#file_obj = tempfile.NamedTemporaryFile()
#file_attributes, filesize = conn.retrieveFile('smbtest', '/rfc1001.txt', file_obj)

# Retrieved file contents are inside file_obj
# Do what you need with the file_obj and then close it
# Note that the file obj is positioned at the end-of-file,
# so you might need to perform a file_obj.seek() if you need
# to read from the beginning
#file_obj.close()






'''
print(dir(smb))
print(smb.info('PVDataLog'))
#print(smb.listdir("/"))


[u'file1.txt', u'file2.txt']
# f = smb.open('/file1.txt')
# data = f.read()
# f.close()
# smb.rename(u'/file1.txt', u'/file1.old')



userID = 'Administrator'
password = '2292'
client_machine_name = 'pi'

server_name = '\\pi\d$'
server_ip = '192.168.178.106'

domain_name = 'domainname'

smbUSR = "Administrator" #blank since anonymous
smbPWD = "2292"
smbFILE = "test.txt"
smbSHR = "D$"

def checkSMB(ip):
    try:
        conn = SMBConnection(smbUSR, smbPWD, use_ntlm_v2 = True)
        assert conn.connect(ip, 145)
        file_obj = tempfile.NamedTemporaryFile()
        file_attributes, filesize = conn.retrieveFile(smbFILE)
    except Exception as e:
        print(e)
        return ("Fail")
    finally:
        #file_obj.close()
        pass

checkSMB("192.168.178.106") #the ip address of the server
#The equivalent Linux command to do this is: smbclient //192.168.1.240/Public
'''

