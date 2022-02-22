#!/usr/bin/env python3

import socket


from smb.SMBConnection import *
class SMBClient(object):
    '''
         SMB connection client
    '''
    user_name = ''
    passwd = ''
    ip = ''
    prot = None

    status = False
    samba = None

    def __init__(self, user_name, passwd, ip, port=139):
        self.user_name = user_name
        self.passwd = passwd
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.samba = SMBConnection(self.user_name, self.passwd, '', '', use_ntlm_v2=True)
            self.samba.connect(self.ip, self.port)
            self.status = self.samba.auth_result
        except:
            self.samba.close()

    def disconnect(self):
        if self.status:
            self.samba.close()

    def all_file_names_in_dir(self, service_name, dir_name):
        '''
                 List all file names in the folder
        :param service_name:
        :param dir_name:
        :return:
        '''
        f_names = list()
        for e in self.samba.listPath(service_name, dir_name):
            #if len(e.filename) > 3: (will return some. Document, need to filter)
            if e.filename[0] != '.':
                f_names.append(e.filename)
        return f_names

    def download(self, f_names, service_name, smb_dir, local_dir):
        '''
                 download file 
                 : param f_names: file name
                 : param service_name: Service Name (folder name in SMB)
                 : param SMB_DIR: SMB folder
                 : param local_dir: Local folder
        :return:
        '''
        assert isinstance(f_names, list)
        for f_name in f_names:
            f = open(os.path.join(local_dir, f_name), 'w')
            self.samba.retrieveFile(service_name, os.path.join(smb_dir, f_name), f)
            f.close()
            
            
            
            
            
userID = 'Administrator'
pw = '2292'
dir_name = 'PVDataLog'
server_name = 'pi'
share_name = '\\pi\d$'
server_ip = '192.168.178.106'

