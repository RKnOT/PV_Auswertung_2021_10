#!/usr/bin/env python3
import os
import csv

import re
from glob import glob
import calendar


from datetime import datetime
from dateutil.relativedelta import relativedelta



cwd = os.getcwd()

CSV_Path_O ='/PV_Anlage_Log_Daten/LOG_PV_2016_01_01_Original'
CSV_Path_N ='/PV_Anlage_Log_Daten/'

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
        #print(self.files_name_day_list)
        
        self.read_files(self.wd)
        #p = self.get_day_yield('30.10.2012')
        #print(p)
        #p = self.get_month_yield('05.04.2014')
        #print(p)
        #p = self.get_year_yield('05.06.2012')
        #print(p)
        
    
    #----------
    def debug_file(self):
        self.files_name_day_list = [['2015'], [['2015_04_13.CSV'],['20150413.CSV']]]
            
    #----------
    def read_files(self, wd):
        y =''
        
        for item in self.files_name_day_list:
            if len(item)==1:
                y = item
            else:
                #print(item)
                new_fn = item[0][0]
                old_fn = item[1][0]    
                path = wd + '/'+ old_fn
                
                file = open(path, encoding="latin-1")
                lines = list(file.readlines())
                
                file.close()
                print('Vorbereitung '+ item[0][0])
                '''
                06.07.2020 12:04:19
                17:10:2012 14:48:01  *01n 20 100TL 4 476.9 2.74 1306 514.5 1.34 690 231.1 2.93 
                '''
                y = item[0][0][:4]
                m = item[0][0][5:7]
                d = item[0][0][8:10]
                data_record =''
                el3_6 =  '  *01n 20 100TL 4 ' 
                date_str = d +'.'+m+'.'+y+' '
                ds = date_str.replace(':', '.')
                dy = self.get_day_yield(ds)
                if dy == []:
                    continue
                print(date_str)
                #print(dy)
                telegrams = ''
                for i in range(3, len(lines)):
                    l = lines[i].replace('\n', '')
                    element = l.split(';')
                    
                    if len(element) !=16:
                        continue
                    #print(element)    
                    data_record = date_str + element[0] + el3_6
                    # dc s1
                    data_record += element[1]+ ' '+element[2]+ ' '+element[3]+ ' '
                    # dc s2
                    data_record += element[4]+ ' '+element[5]+ ' '+element[6]+ ' '
                    # ac p1
                    data_record += element[7]+ ' '+ element[8]+ ' '
                    # ac p2
                    data_record += element[9]+ ' '+ element[10]+ ' '
                    #ac p3
                    data_record += element[11]+ ' '+element[12]+ ' '
                    # dc power / ac power / cosph
                    data_record += element[13]+ ' '+element[14]+ ' 1.000 ' 
                    # temperatur / maxpower / crc
                    data_record += element[15]+ ' ' +dy[1] +' 0000 \n'
                    
                    #print(data_record)
                    telegrams += data_record
                #print(telegrams)
                
                file_write_name = self.wd_new+'/'+y +'/'+item[0][0]
                
                
                f = open(file_write_name , "w")
                f.write(telegrams)
                f.close()
                print('file:  '+ item[0][0] + ' geschrieben')
                #open and read the file after the appending:
                #f = open(file_write_name, "r")
                #print(f.read())
                
                #return
                
    
    #-------------------------
    def get_year_yield(self, date_str):
        try:
            ind = self.years_yield_list.index([date_str[-4:]])
            year_selected = self.years_yield_list[ind+1]
            #print(year_selected)
            sum = 0.0
            count = 0
            for item in year_selected[1]:
                try:
                    sum += float(item)
                    count += 1
                except:
                    pass
            sum /= 1000
            dt = datetime .strptime(date_str, '%d.%m.%Y').date()
            sum_str = "{0:.3f}".format(sum)
            para = [date_str, sum_str, dt, sum, count]
            
        except ValueError:
            para = []
        return para
    #-------------------------
    def get_month_yield(self, date_str):
        try:
            ind = self.month_yield_list.index([date_str[3:]])
            month_selected = self.month_yield_list[ind+1]
            #print(month_selected[1])    
            sum = 0.0
            count = 0
            for item in month_selected[1]:
                try:
                    sum += float(item)
                    count += 1
                except:
                    pass
                sum /= 1000
                dt = datetime .strptime(date_str, '%d.%m.%Y').date()
                sum_str = "{0:.3f}".format(sum)
                para = [date_str, sum_str, dt, sum, count]
        except ValueError:
            para = []
        return para  
    #-------------------------
    def get_day_yield(self, date_str):
              date_str = date_str.strip()
              try:
                  ind = self.month_yield_list.index([date_str[3:]])
                  #print(ind)
                  month_selected = self.month_yield_list[ind+1]
                  #print(month_selected)
                  dt = datetime .strptime(date_str, '%d.%m.%Y').date()
                  try:
                      ind = month_selected[0].index(date_str)
                      datestr = month_selected[0][ind]                           
                      
                      yield_tpower_float = float(month_selected[1][ind])
                      yield_tpower_str=month_selected[1][ind]
                      #yield_tpower_str = "{0:.3f}".format(yield_tpower_float)
                      para = [datestr, yield_tpower_str, dt, yield_tpower_float]
                  # no day record in month view
                  except ValueError:
                      para =[date_str, '0', dt, 0.0]
              except ValueError:
                  para = []
              #print(para)
              return para    
              #-----------
              # add one day
              #dt = datetime .strptime(date_str, '%d.%m.%Y').date()
              #dt = dt+ relativedelta(day=1)
              
    
    #----------    
    def get_set_dir_and_rename_files(self, cwd):
        os.chdir(self.wd)
        CSV_Path = glob('*')
        CSV_Path.sort()
        # set dirs & rename filename
        year = ''
        y = ''
        ym =''
        m = ''
        
        for item in CSV_Path:
            # day file name list
            if(len(item) == 12):
                year = item[0:4]
                month = item[4:6]
                day = item[6:8] 
                if y != year:
                    y = year
                    self.files_name_day_list.append([year])
                    # make dir in case of not exists
                    if os.path.exists(parent_dir_N + year) == False:
                        path = os.path.join(parent_dir_N, year)
                        os.mkdir(path)
                self.files_name_day_list.append([[year +'_'+month+'_'+day+'.CSV'], [item]])
            #-------------
            # month yield list
            if len(item) == 10:
                year = item[0:4]
                month = item[4:6]
                if month != m:
                    m= month
                    self.month_yield_list.append([month+'.'+year])
                path = self.wd + '/'+ item
                
                with open(path) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=';')
                    dates = []
                    yields = []
                    for row in readCSV:
                        if len(row) ==2:
                            ertrag = row[1]
                            date = row[0]
                            dates.append(date.replace('/','.'))
                            yields.append(ertrag)

                self.month_yield_list.append([dates, yields])
                #print(dates)
                #print(yields)
            #-----------------
            
            # year yield list
            if len(item) == 8:
                year = item[0:4]
                if ym != year:
                    ym = year
                    self.years_yield_list.append([year])
                path = self.wd + '/'+ item
                
                with open(path) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=';')
                    dates = []
                    yields = []
                    for row in readCSV:
                        if len(row) ==2:
                            ertrag = row[1]
                            date = row[0]
                            dates.append(date)
                            yields.append(ertrag)
                self.years_yield_list.append([dates, yields])       
            #------
        
      
        
        
        
        
        #print(self.month_yield_list)
        #print(self.years_yield_list)    
        os.chdir(cwd)
        
                
                                                  
                                                                                                    
    #-------           
                
        
#--------------------        
        
        
        
        
get_file_names = GetCSV_Dir_and_File_Names(cwd, CSV_Path_O, CSV_Path_N)
#print (get_file_names.years_list)
#print(get_file_names.files_name_list)


#----------------------------------
