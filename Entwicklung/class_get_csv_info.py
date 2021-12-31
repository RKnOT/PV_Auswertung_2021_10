#!/usr/bin/env python3
import os
from glob import glob
import datetime





class GetCSVFilesStatus():
    def __init__(self, CSV_Path, dstr, ext = 'CSV'):
        self.dic_years ={}
        self.record_flag = False
        self.status = 'der Record '+ dstr + ' ist nicht vorhanden'
        d_datum = self.get_date(dstr)
        CWD = os.getcwd()
        os.chdir(CSV_Path)
        CSV_Path = glob('*')
        year_dirs =[]
        for item in CSV_Path:
            year_dirs.append(item)
        self.dic_years = self.set_dic(year_dirs)
        os.chdir(CWD)
        len = self.date_is_in_List(self.dic_years, d_datum)
        if len ==1:
            self.status = 'der Record '+ dstr + ' ist vorhanden'
            self.record_flag = True
    #-------------------------
    def date_is_in_List(self, dict, datum):
        yearstr = str(datum.year)
        t_stat = 0
        if str(yearstr) in dict: 
            y_flag = True 
            flist = dict[yearstr] 
            t = list(filter(lambda x: x == datum, flist))
            t_stat = len(t)
        return t_stat
    #-------------------------
    def set_dic(self, ly, ext ='CSV'): 
        dyears ={}
        for item in ly:
            wd = os.getcwd()
            lt = []
            p = wd + '/'+item  
            os.chdir(p)
            files = glob('*.'+ext)
            for item1 in files:
              datum_str = os.path.splitext(os.path.basename(item1))[0]
              dateObj = self.get_date(datum_str)
              if str(dateObj.year) == item:
                   lt.append(dateObj)
            lt.sort() 
            dyears[item] = lt   
            os.chdir(wd)
        return dyears
    #-------------------------
    def get_date(self, dstr):
        dObj = datetime.datetime.strptime(dstr, "%Y_%m_%d").date()
        return dObj
    

path_csvFiles = "PVDataLog"
datestr = '2021_03_01'
c1 = GetCSVFilesStatus(path_csvFiles, datestr)
print(c1.status)
print(c1.record_flag)
print(c1.dic_years)