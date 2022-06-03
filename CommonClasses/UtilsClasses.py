
#!/usr/bin/env python3

#python -m pip install --upgrade pip
# pip install pandas

import os
import sys
import platform
import shutil
import json

from pathlib import Path
import numpy as np
import csv
import re
import datetime
import calendar

fpath = '/private/var/mobile/Containers/Shared/AppGroup/FA16265D-A93E-42FB-9932-E3CC306D50A8/File Provider Storage/Repositories/Python_Utils/Date_Time_Utils'
sys.path.append(fpath)

import date_time_util as dtu
dt = dtu.helpers_date_utils()






from datetime import date, time, datetime
from scandir import scandir, walk



debug_SMB_flag = False



import uuid
platform_flag = True # True windows // false IOS
if platform.system() != 'Windows':
    platform_flag = False
    try:
        from smbprotocol.connection import Connection, Dialects
        from smbclient import (listdir, mkdir, register_session, rmdir, scandir,)
    except:
        if debug_SMB_flag == True:
        	print('smb protocol konnte nicht gestartet werden')
        
    
   
    
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
         self.root = ''
         
         self.data = ini
         
   #--------Server Daten-----------------

   
   def iniData(self):
         
         #defining a function to find index in a list using lambda
         get_indexes = lambda x, searchable: [i for (y, i) in zip(searchable, range(len(searchable))) if x == y]
         
         #get root dir
         #private/var/mobile/Containers/Shared/AppGroup/FA16265D-A93E-42FB-9932-E3CC306D50A8/File Provider Storage/Repositories/PV_Auswertung_2021_10
        
         
         
         p = str(Path(__file__).parents[0])
         p_list = p.split("/")
         index_1 = len(p_list)
         index_2 = get_indexes('Repositories', p_list)[0]
         root_index = index_1 - index_2 - 2
         self.root = str(Path(__file__).parents[root_index])
         #print(root)
         #print('-.-.-.-')

         dir_CSV = 'PVDataLog'
         
         dir = dir_CSV + '/' + str(datetime.now().year)
         self.dir_local_CSV = self.root + '/'+ dir_CSV
         
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
                      'dir_name' : dir_CSV,
                      'dir_name_local' : self.root + '//' + dir
                      }
                   }
                   
                   
         if platform_flag == True: # platform windows
             data['Local']['dir_name_local'] = root + '\\PVDataLog\\' + str(datetime.today().year)          
         #print(',,*******,,,,,,')          
         #print(data['Local']['dir_name_local'])
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

        nd = NetworkData([], True)

        try:
            import smbclient
            smbclient.ClientConfig(username = nd.user, password= nd.pw)
            smbclient.register_session(nd.server, username= nd.user, password=nd.pw)
        except:
            print('smbclient konnte nicht gestartet werden')    
        for i, j, in enumerate(fnamesTB):
            source = nd.share + '\\' + nd.dir_name + '\\' + j[0]
            #print(source)
            dest = nd.dir_name_local + '/' + j[0]
            #print(dest)
            if platform_flag == False:
                with smbclient.open_file(source, mode="r") as fd:
                    file_content = fd.read()
                with open(dest, 'w') as f:
                    f.write(file_content)
                self.count +=1
            else: #Windows
               shutil.copyfile(source, dest)
            self.copied_files.append('file: '+ j[0] + ' copied')
        

#-------------------------
class Get_CSV_File_Names_from_Dir():
		def __init__(self, selected_years = ['']):
			self.stat = ''
			self.years_month_days_dic = {}
			self.years_list = []
			sorted_file_names =[]
			
			I_Get_CSV_File_Names = Get_CSV_File_Names(get_files_flag = False)
			
			# I_Get_CSV_File_Names.nd.dir_local_CSV -> directory of CSV`s
			if selected_years[0] == '':
				self.years_list = list(filter(lambda x : len(x) == 4 , sorted(os.listdir(I_Get_CSV_File_Names.nd.dir_local_CSV)) ))
			else:
				 self.years_list = selected_years
			#print(self.years_list)
			
			for item in self.years_list:
				CSVs_Dir = I_Get_CSV_File_Names.nd.dir_local_CSV + '/' + item
				I_Get_CSV_File_Names.get_from_dir_file_names(CSVs_Dir, '.CSV')
				sorted_file_names.append(I_Get_CSV_File_Names.fl)
			#print(I_Get_CSV_File_Names.fl)
			self.get_available_years_month_days(self.years_list, sorted_file_names)
			#print(self.years_month_days_dic)
			
		def get_available_years_month_days(self, years, csv):
			for i in range(0, len(years)):
				m_list = self.get_available_month(csv[i])
				#print(m_list)
				month_days = self.get_available_days(csv[i], m_list)
				#print(month_days)
				self.years_month_days_dic[years[i]] = month_days
			#print(self.years_month_days_dic)
					
		def get_available_month(self, list_year):
			list_csv_records =[]
			list_available_month =[]
			#get from date_time_util empty month_list
			m_list = dt.get_month_list()
			for item in m_list:
				result = list(filter(lambda x: item in x, list_year))
				if result != []:
					list_available_month.append(item[1:-1])
			#print(list_available_month)
			return list_available_month
				
		def get_available_days(self, list_year, year_month):
			#print(list_year)
			#print(year_month)
			month_days_dic = {}
			for item in year_month:
				i = '_' + item + '_'
				result = list(filter(lambda x: i in x, list_year))
				#print(result)
				days = list(map(lambda x :x[8:10] , result))
				#print(days)
				month_days_dic[item] = days
			#print(month_days_dic)	
			return month_days_dic
				
			
#-------------------------
class Get_CSV_File_Names():
    def __init__(self, dir = '', ext ='.CSV', get_files_flag = True):
        self.cwd_dir = ''
        self.fileNamesSizeTublesArray = ''
        self.stat=''
        self.fl =[]
        self.fl_fs = []
        if dir == '':
            self.nd = NetworkData([], True)
            self.PVDateien = self.nd.dir_name_local
            #print(self.PVDateien)
        if(get_files_flag):
        	self.get_from_dir_file_names(self.PVDateien, ext)
            
    def get_from_dir_file_names(self, dir, ext):
        #print(dir)
        cwd = os.getcwd()
        #print(cwd)
        try:
            
            #-------------- check year dir exists locally------
            if os.path.isdir(self.nd.dir_name_local) == False:
                os.mkdir(dest)
            
        #---------------------------------------------------
        
            
            #print(dir)
            os.chdir(dir)
            self.dir_files = os.getcwd()
            #print(os.listdir())
            self.fl  = sorted(list(filter(lambda x: x if ext in x else [], os.listdir())))
            self.fileNamesSizeTublesArray  = list(map(lambda x: (x, os.path.getsize(x)), self.fl))
            self.stat = f'{len(self.fl)} files mit der Extension: {ext} gefunden'
            #print(self.stat)
        except:
            self.fl.append(-1)
            self.fileNamesSizeTublesArray(-1)
            self.dir_files = os.getcwd() + '/' + dir
            self.stat = 'directory does not exists:\n' + self.dir_files
        finally:
            os.chdir(cwd)
            self.cwd_dir = os.getcwd()
#---------------------------

#test
'''
file_to_copy = '2022_03_08.CSV'
nd = NetworkData([], True)
local_dir_file = nd.dir_name_local + '/'+ file_to_copy
print(local_dir_file)




nw_dir = nd.share + '\\' + nd.dir_name + '\\' + file_to_copy
print(nw_dir)

import smbclient

# Optional - specify the default credentials to use on the global config object
smbclient.ClientConfig(username = nd.user, password= nd.pw)

# Optional - register the credentials with a server (overrides ClientConfig for that server)
smbclient.register_session(nd.server, username= nd.user, password=nd.pw)


with smbclient.open_file(nw_dir, mode="r") as fd:
    file_content = fd.read()

with open(local_dir_file, 'w') as f:
    f.write(file_content)





loc = Get_CSV_File_Names()
CSV_local = loc.fileNamesSizeTublesArray
rem = GetNWCSV_File_Names()
CSV_remote = rem.fileNamesSizeTublesArray
#print(CSV_remote)
   
fToCopy = CompareSameFilesRemoteAndLocal(CSV_remote, CSV_local)

print(fToCopy.fileToUpdate)



copyFile = CopyNWfilesToLocal(fToCopy.fileToUpdate)
print(copyFile.copied_files)
'''
    
   
