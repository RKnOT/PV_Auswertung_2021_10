#!/usr/bin/env python3

import os
from console import clear
import csv
import re
import math
from datetime import date, datetime, timedelta

import calendar

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.dates import DateFormatter

from DataModel import TagUtil as TagRecord
from DataModel import GetCSV_File_Names as GetCSV_Names


        
#------------------
class YearView():
    def __init__(self, csv):
        #print(csv.status)
        #print(csv.selected_Year_Files)
        self.A=''
        self.tpy=''
        self.yv(csv)
        
        
    def yv(self, csv):
        dm = TagRecord()
        self.A, self.tpy = dm.getYearValues(csv.selected_Year_Files) 
        
        
        
#----------------------        
class MonthView():
    
    def __init__(self, csv):
        self.CSV = csv
        #print(csv.dic_year)
        self.A=''
        self.monthYield =''
        self.mv(csv.selected_Month_Files)
        
    def mv(self, csv):
        dm = TagRecord() 
        self.A, self.monthYield = dm.getAllLastTelegrams(csv)
        
#----------------------               
class DayView():
   
    def __init__(self, csv, TeleSelected):
        self.CSV = csv
        #print(csv.status)
        #print(csv.selected_Day_File)
        self.A=''
        self.tpowerStr = ''
        self.max_ACPower = ''
        self.dv(csv.selected_Day_File, TeleSelected)
        
    def dv(self, dayrecord, TeleSelected):
        dm =TagRecord()
        self.A, self.tpowerStr, self.max_ACPower= dm.getAllDayTelegramms(dayrecord, TeleSelected) 
        