#!/usr/bin/env python3
import os
import csv
import re
from glob import glob
import datetime


#p1 = os.getcwd()
#print(p1)

path_csvFiles = "PVDataLog"

CWD = os.getcwd()
os.chdir(path_csvFiles)

paths = glob('*')


os.chdir(CWD)

year_dirs =[]

for item in paths:
    year_dirs.append(item)

#print(year_dirs)

dic_years ={}
for item in year_dirs:
    wd = os.getcwd()
    lt = []
    p = path_csvFiles + '/'+item  
    os.chdir(p)
    files = glob('*.CSV')
    for item1 in files:
      datum_str = os.path.splitext(os.path.basename(item1))[0]
      dateObj = datetime.datetime.strptime(datum_str, "%Y_%m_%d").date()
      if str(dateObj.year) == item:
       lt.append(dateObj)
    lt.sort() 
    dic_years[item] = lt   
    os.chdir(wd)

os.chdir(CWD)

p1 = os.getcwd()
print(p1)



#--------


lk = list(dic_years.keys())
lv = list(dic_years.values())

#print(dic_years)

print(dic_years['2020'])
print('-----')

print(dic_years.keys())

print('-----')
print(lk)

print('-----')
print(lv[0])


