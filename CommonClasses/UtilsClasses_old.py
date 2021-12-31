
#!/usr/bin/env python3
import os

import json

import csv
import re
import datetime
import calendar

from datetime import date, time, datetime

from scandir import scandir, walk
from smbclient import (listdir, open_file, mkdir, register_session, rmdir, scandir)

#------- class Network Data start------
jsonDat = 'NetworkParameter.json'

class NetworkData():
   def __init__(self, ini = [], resetData = False, overWriteJson = False):
         debug = False
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
         fe = list(ini) 
         a = ini[fe[0]]
         b = ini[fe[1]]
         if debug: print(a[0]['port'])
         self.server = a[0]['server']
         self.port = a[0]['port'] 
         self.user = a[0]['user']
         self.pw = a[0]['pw']
         self.share = a[0]['share']
         self.dir_name = a[0]['dir_name']
         
         self.dir_name_local = b[0]['dir_name_local']
         
         self.data = ini
         
   #--------Server Daten-----------------
   def iniData(self):
         dir = 'PVDataLog/' + str(datetime.now().year)
         data = {}
         data['Server'] =[]
         data['Server'].append({
                'server' : 'pi',
                'port' : 445,
                'user' : 'Administrator',
                'pw' : '2292',
                'share' : r'\\pi\d$',
                'dir_name' : 'PVDataLog',
                })
         
         data['Local'] =[]
         data['Local'].append({
                'dir_name_local' : dir,
                })
         return data
   #---------read write json-------------         
   def writeJsonFile(self, ini):
         with open(jsonDat, 'w') as outfile:
                json.dump(ini, outfile)
   def readJsonFile(self):  
       if os.path.exists(jsonDat):
           with open(jsonDat) as json_file:
                self.data = json.load(json_file)
       else: self.data =[]
#------- class Network Data end------

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
#----------------------------        
class GetNWCSV_File_Names():
    
    def __init__(self):
        str_year = str(datetime.now().year)
        nd = NetworkData([], True)
        self.workingDir = nd.share +'\\' + nd.dir_name
        self.fileNamesSizeTublesArray = []
        register_session(nd.server, username = nd.user, password = nd.pw)
        for entry in scandir(self.workingDir):
            s = entry.stat(entry.name)
            sp = entry.name.split('_')
            ft =False
            if sp[0] == str_year: ft=True
            #print(sp[0])
            if entry.name.endswith('.CSV') & ft:
               self.fileNamesSizeTublesArray.append((entry.name, s.st_size))
        self.fileNamesSizeTublesArray.sort(reverse = False)            
            
                
#-------------------------
class CopyNWfilesToLocal():
    def __init__(self, fnamesTB):
        nd = NetworkData([], True)
        self.count = 0
        self.workingDir = nd.share +'\\' + nd.dir_name
        path_parent = os.getcwd()+'/'
        print(path_parent)
            
        for i, j, in enumerate(fnamesTB):
            source = self.workingDir + '\\' + j[0]
            #print(source)
            dest = path_parent + nd.dir_name_local + '/' + j[0]
            #print(dest)
            register_session(nd.server, username= nd.user, password = nd.pw)
            with open_file(source, username = nd.user, password = nd.pw, mode ='r') as fd:
                file_contents = fd.read()
                #print(len(file_contents))
                destFile = open(dest, 'w')
                destFile.write(file_contents)
                destFile.close()
                print('file: '+ j[0] + ' copied')
                self.count += 1 
        

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
        try:
            cwd = os.getcwd()
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



