#!/usr/bin/env python3
import os
import sys
import csv

import re
from glob import glob
import calendar


from datetime import datetime
from dateutil.relativedelta import relativedelta


cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')

from CommonClasses.DataModel import PV_Telegram as Telegram

CSV_Path_O ='/LOG_MEGA_128'
CSV_Path_N ='/LOG_MEGA_128/2014'

parent_dir_O = cwd + CSV_Path_O
parent_dir_N = cwd + CSV_Path_N

os.chdir(parent_dir_O)

#------------------------
class GetCSV_Dir_and_File_Names():
    def __init__(self, cwd, csv_dir_name, csv_dir_name_new):
        self.files_name_day_list = []
        self.day_yield_list =[]
        self.month_yield_list =[]
        self.years_yield_list = []
        
        self.wd = os.path.join(cwd + csv_dir_name)
        self.wd_new = os.path.join(cwd + csv_dir_name_new)
        self.get_set_dir_and_rename_files(cwd)
        #self.debug_file()
        self.read_file_content()
    
    #----------
    def debug_file(self):
        self.files_name_day_list = [['2014'], [['2014_04_16.CSV'],['20140416.CSV']]]
            
    #----------
    
    def read_file_content(self):
        #print(self.files_name_day_list[0])
        
        for item in self.files_name_day_list:
            #print(item)
        
            path = os.path.join(self.wd, item)
            #print(path)
            file = open(path, encoding="latin-1")
            lines = list(file.readlines())
            file.close()
            count=0
            #print(len(lines))
            for i in lines:
                dr = Telegram()
                dr.get_Tele_Values(i)
                if dr.stat_flag: 
                    count +=1
                
                #print(dr.stat)
                
            if count == len(lines):
                print(item + ' teles are ok')   
            
                       
        
        '''
        
        nl =[]
        for item in lines:
            x = item.strip() + '\n'
            nl.append(x)
        #print(nl)
        
        f = open(path_01 , "w")
        for x in nl: 
            f.write(x)
        f.close()
        '''
        
    #----------    
    def get_set_dir_and_rename_files(self, cwd):
        os.chdir(self.wd)
        self.files_name_day_list = glob('*')
        self.files_name_day_list.sort()
        #print(self.files_name_day_list)
        # set dirs & rename filename
        year = ''
        y = ''
        ym =''
        m = ''
        for item in self.files_name_day_list:
            #print(item)
            if(len(item) == 12 and item[9:]== 'txt'):
                year = '20'+item[0:2]
                month = item[3:5]
                day = item[6:8] 
                #print(year)
                #print(month)
                #print(day)
                nf = year+'_'+ month +'_'+day+'.CSV'
                old_file = os.path.join(self.wd, item)
                new_file = os.path.join(self.wd, nf)
                #print(old_file)
                print(new_file)
                os.rename(old_file, new_file)
                #return
        
        
        
        
get_file_names = GetCSV_Dir_and_File_Names(cwd, CSV_Path_O, CSV_Path_N)
#print (get_file_names.years_list)
#print(get_file_names.files_name_list)


#----------------------------------
