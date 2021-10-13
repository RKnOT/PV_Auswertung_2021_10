import os
import sys

from datetime import datetime

cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')

from CommonClasses.DataModel import GetCSV_File_Names as GetCSV_Names

#---------------------
class sub_dir_Names():
    def __init__(self):
        self.path_csvFiles = "PVDataLog"
        #---
        self.CSV_Path_O_Log ='/PV_Anlage_Log_Daten/LOG_PV_2016_01_01_Original'
        self.CSV_Path_N_Log ='/PV_Anlage_Log_Daten/'
        #---
        self.CSV_Path_O_Mega ='/LOG_MEGA_128'
        self.CSV_Path_N_Mega ='/LOG_MEGA_128/2014'

#------------------
class check_CSV(sub_dir_Names):
    def __init__(self, Ds, Ms, Ys, print_flag = False):
        super().__init__()
        #path_csvFiles = "PVDataLog"
        datestr = str(Ys) +'_'+ str(Ms).zfill(2)+ '_'+ str(Ds).zfill(2)
        #print(datestr)    
        try:
            dt = datetime .strptime(datestr, '%Y_%m_%d').date()
            #print(dt)
        except:
            print('falsches Datum')
            datestr ='2013_03_19'
        #print(dt)
        self.csv = GetCSV_Names(self.path_csvFiles, datestr)
        if self.csv.year_record_flag == False:
            print('falsches Datum')
            
        if print_flag: print(self.csv.status)

#------------------------
