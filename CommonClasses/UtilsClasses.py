
#!/usr/bin/env python3
import os
import platform
import shutil
import json

import csv
import re
import datetime
import calendar

from datetime import date, time, datetime
from scandir import scandir, walk


#a=GetNWCSV_File_Names()
import uuid
platform_flag = True # True windows // false IOS
if platform.system() != 'Windows':
    platform_flag = False
    from smbclient import (listdir, open_file, mkdir, register_session, rmdir, scandir)

#------- class Network Data start------
jsonDat = 'NetworkParameter.json'

class NetworkData():
   def __init__(self, ini = [], resetData = False, overWriteJson = False):
         debug = False
         self.data =[]
         if resetData:
             ini = self.iniData()
             
             overWriteJson = True
             if debug: print('reset Data')  
         else: 
             if ini == []:
                 self.readJsonFile()
                 if self.data ==[]:
                     ini = self.iniData()
                     if debug: print('no jsonfile')
                     overWriteJson = True
                 else: 
                     ini = self.data
                     if debug:   print('from jsonfile')
             
         if overWriteJson:
             self.writeJsonFile(ini)
             if debug: print('jsonfile written')
         
         if debug:   print(ini)
          
         a = ini['Server']
         b = ini['Local']
         if debug: print(a['port'])
         self.server = a['server']
         self.port = a['port'] 
         self.user = a['user']
         self.pw = a['pw']
         
         self.dir_name_local = b['dir_name_local']
         self.share = b['share']
         self.dir_name = b['dir_name']
         
         
         self.data = ini
         
   #--------Server Daten-----------------
   
   
   def iniData(self):
         dir = 'PVDataLog/' + str(datetime.now().year)
         
         data = { 'Server' : 
                     { 
                      'server' : 'pi', 
                      'port' : 445, 
                      'user' : 'Administrator', 
                      'pw' : '2292', 
                     },
                  'Local' :
                     {
                      'share' : r'\\pi\d$', 
                      'dir_name' : 'PVDataLog',
                      'dir_name_local' : 'PVDataLog/' + str(datetime.today().year)
                      }
                   }
                   
                   
         if platform_flag == True: # platform windows
             data['Local']['dir_name_local'] = os.curdir() + '\\PVDataLog\\' + str(datetime.today().year)          
                   
         
         return data
   
   
   #---------read write json-------------         
   def writeJsonFile(self, ini):
         
        #with open(jsonDat, 'w') as outfile:
         #       json.dump(ini, outfile)
         pass
   def readJsonFile(self):  
       #if os.path.exists(jsonDat):
        #   with open(jsonDat) as json_file:
         #       self.data = json.load(json_file)
       #else: self.data =[]
       pass
#------- class Network Data end------

#------- class Network get files under windows environment

class Get_Write_Windows_Network_Files():
    def __init__(self, ext = '.CSV'):
        nd = NetworkData([], True)
        self.PVDir = nd.share + '/' + nd.dir_name
        Dir_names = os.listdir(self.PVDir)
        current_year = str(datetime.now().year)
        self.fl = list(filter(lambda x : (ext in x and current_year in x), Dir_names))
        self.fileNamesSizeTublesArray  = list(map(lambda x: (x, os.path.getsize(self.PVDir + '/'+x)), self.fl))
        #print(len(self.fileNamesSizeTublesArray ))
        #print(len(self.fl))

       

#--------------------------
class CompareSameFilesRemoteAndLocal():
    def __init__(self, Master, Slave):
        self.fileToUpdate = []
        #self.fileToUpdate.append(('filename', 'filesize', 'index', 'comment'))
        #-----Lamda function------
        # defining a function to find index in a list using lambda
        get_indexes = lambda x, searchable: [i for (y, i) in zip(searchable, range(len(searchable))) if x == y]
        #----end lamda fumctiom----
        
        master_name_List =[]
        slave_name_List =[]
        
        for item in Slave:
            slave_name_List.append(item[0])
        for item in Master:
            master_name_List.append(item[0])
        for item in master_name_List:
            rindex = master_name_List.index(item)
            index = get_indexes(item, slave_name_List)
            fs = Master[rindex][1] 
            if index == []:
                self.fileToUpdate.append((item, fs, rindex, 'no local File'))
            else:
                lindex = slave_name_List.index(item)
                sFs = Slave[lindex][1]
                mFs = Master[rindex][1]
                if sFs != mFs:
                    self.fileToUpdate.append((item, fs, rindex, 'diff file size'))
        #print(self.fileToUpdate)
                
#-------------------------

class GetNW():
    
    def __init__(self):
        
        self.status_NW_flag = False
        nd = NetworkData([], True)
        self.NW_data = nd.data['Server']
        try:
            s = register_session(nd.server, username = nd.user, password = nd.pw)
            self.status_NW_flag = True
        except:
            pass
            
        
#----------------------------        
class GetNWCSV_File_Names():
    
    def __init__(self):
        str_year = str(datetime.now().year)
        nd = NetworkData([], True)
        self.workingDir = nd.share +'\\' + nd.dir_name
        
        #print(self.workingDir)
        #print(nd.dir_name_local)
        self.fileNamesSizeTublesArray = []
        #print('####---------#######')
        register_session(nd.server, username = nd.user, password = nd.pw)
        for entry in scandir(self.workingDir):
            s = entry.stat(entry.name)
            sp = entry.name.split('_')
            ft = False
            if sp[0] == str_year: ft=True
            if entry.name.endswith('.CSV') & ft:
                self.fileNamesSizeTublesArray.append((entry.name, s.st_size))

               
        self.fileNamesSizeTublesArray.sort(reverse = False)
        #print(len(self.fileNamesSizeTublesArray))
        #print('----    ----')            
            
                
#-------------------------
class CopyNWfilesToLocal():
    def __init__(self, fnamesTB, copy_Files = True):
        nd = NetworkData([], True)
        self.count = 0
        self.copied_files =[]
        self.workingDir = nd.share +'\\' + nd.dir_name
        path_parent = os.getcwd()+'/'
        #print(path_parent)
        if copy_Files == False:
            return 

        for i, j, in enumerate(fnamesTB):
            source = self.workingDir + '\\' + j[0]
            #print(source)
            dest = path_parent + nd.dir_name_local + '/' + j[0]
            #print(dest)
            if platform_flag == False:
                register_session(nd.server, username= nd.user, password = nd.pw)
                with open_file(source, username = nd.user, password = nd.pw, mode ='r') as fd:
                    #shutil.copyfile(source, dest)
                    
                    file_contents = fd.read()
                    #print(len(file_contents))
                    destFile = open(dest, 'w')
                    destFile.write(file_contents)
                    destFile.close()
                    self.count +=1
                    
            else: #Windows
               shutil.copyfile(source, dest)
            self.copied_files.append('file: '+ j[0] + ' copied')
        

#-------------------------

class Get_CSV_File_Names():
    def __init__(self, dir = '', ext ='.CSV'):
        self.cwd_dir = ''
        self.fileNamesSizeTublesArray = ''
        self.stat=''
        self.fl =[]
        self.fl_fs = []
        if dir == '':
            nd = NetworkData([], True)
            self.PVDateien = nd.dir_name_local
        self.get_from_dir_file_names(self.PVDateien, ext)
            
    def get_from_dir_file_names(self, dir,ext):
        cwd = os.getcwd()
        try:
            
            #-------------- check year dir exists locally------
        
       
            nwd = NetworkData()
            dest = os.getcwd() + '/' + nwd.dir_name_local
            if os.path.isdir(dest) == False:
               os.mkdir(dest)
        #---------------------------------------------------
        
            
            #print(dir)
            os.chdir(dir)
            self.dir_files = os.getcwd()
            self.fl  = list(filter(lambda x: x if ext in x else [], os.listdir()))
            self.fileNamesSizeTublesArray  = list(map(lambda x: (x, os.path.getsize(x)), self.fl))
            self.stat = f'{len(self.fl)} files mit der Extension: {ext} gefunden'
        except:
            self.fl.append(-1)
            self.fileNamesSizeTublesArray(-1)
            self.dir_files = os.getcwd() + '/' + dir
            self.stat = 'directory does not exists:\n' + self.dir_files
        finally:
            os.chdir(cwd)
            self.cwd_dir = os.getcwd()
#---------------------------
#a = GetNWCSV_File_Names()

nd = NetworkData([], True)
workingDir = nd.share +'\\' + nd.dir_name
        
print(workingDir)
print(nd.dir_name_local)
fileNamesSizeTublesArray = []
print('####---------#######')

register_session(nd.server, username = nd.user, password = nd.pw)
        


