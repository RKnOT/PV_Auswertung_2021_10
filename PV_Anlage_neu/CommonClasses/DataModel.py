#!/usr/bin/env python3
import os
import csv
import re
from glob import glob
import calendar


from datetime import datetime
from matplotlib import pyplot as plt


class Utils():
   
    def getDateTimeZero(self, dt):
        return datetime.combine(dt, datetime.min.time())
   
    
#--------------------------------
+   #print(CSV_Path)
        #print(dstr)
        self.dic_years = {}
        self.dic_year = {}
        self.selected_Day_File = ''
        self.selected_Month_Files = {}
        self.selected_Year_Files = {}
        self.available_Years = []
        self.path = ''
        self.day_record_flag = False
        self.month_record_flag = False
        self.year_record_flag = False
        self.status = 'der Tag-Record '+ dstr + ' ist nicht vorhanden'
        d_datum = self.get_date(dstr)
        CWD = os.getcwd()
        os.chdir(CSV_Path)
        CSV_Path = glob('*')
        year_dirs =[]
        #print(os.listdir('.'))
        for x in os.listdir('.'):
            self.available_Years.append(x)
        self.available_Years.sort()
        try:
            ind = self.available_Years.index(dstr[:4])
        except:
            ind =-1
            return 
        
        for item in CSV_Path:
            year_dirs.append(item)
        self.dic_years = self.set_dic(year_dirs)
        list_year, list_month, list_day = self.date_is_in_List(self.dic_years, d_datum)
        #print(list_year)    
        #print(list_month)
        self.path = os.getcwd()+ '/'+ str(d_datum.year)+'/'
        if list_day  != []:
            self.day_record_flag = True
            self.month_record_flag = True
            self.year_record_flag = True
            self.dic_year = self.dic_years[str(d_datum.year)]    
            self.status = 'der Tag-Record '+ dstr + ' ist vorhanden'
            self.year_record_flag = True
            self.selected_Day_File = self.path + dstr + '.' + ext
            self.get_selected_Month_List(d_datum, ext)
            self.get_selected_Year_List(ext)
        elif list_month != []:
            self.month_record_flag = True
            self.year_record_flag = True
            self.status = 'Monat-Records '+ str(d_datum.month)+ '/' +str(d_datum.year) + ' sind vorhanden'
            self.dic_year = list_year
            self.get_selected_Month_List(d_datum, ext)
            self.get_selected_Year_List(ext)
        elif list_year != []:
            self.year_record_flag = True
            self.status = 'Jahr-Records '+ str(d_datum.year) + ' sind vorhanden'
            self.dic_year = list_year
            self.get_selected_Year_List(ext)
        os.chdir(CWD)
    
    #-------------------------
    def get_selected_Year_List(self, ext):
        l = []
        for item in self.dic_year:
            l.append(item.strftime('%Y_%m_%d')+'.'+ext)
        self.selected_Year_Files[self.path]= l
        #print(self.dic_year)
    #-------------------------
    def get_selected_Month_List(self, datum, ext):
        l = []
        #print(self.dic_year)
        for item in self.dic_year:
            if item.month == datum.month:
                #print(item.strftime('%Y_%m_%d'))
                l.append(item.strftime('%Y_%m_%d')+ '.'+ext)
        self.selected_Month_Files[self.path] = l             
        #print(self.selected_Month_Files)
    #-------------------------
    def date_is_in_List(self, dict, datum):
        yearstr = str(datum.year)
        t_stat = 0
        t_month =[]
        if str(yearstr) in dict: 
            flist = dict[yearstr] 
            t_year = list(filter(lambda x: x.year == datum.year, flist))
            t_month = list(filter(lambda x: x.month == datum.month, flist)) 
            t_day = list(filter(lambda x: x.day == datum.day, t_month))
        return t_year, t_month, t_day
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
        #print(dstr)
        dObj = datetime.strptime(dstr, "%Y_%m_%d").date()
        return dObj
#-- Start Class PV_Telegram-------------
        

from collections import namedtuple
from datetime import date, time, datetime

import numpy as np

class Date_Format():
    def __init__(self):
        self.strTimeFormat = '%d.%m.%Y %H:%M:%S'
        
    def str_to_date(self, dstr):
        dt = datetime.strptime(dstr, self.strTimeFormat)  
        return dt
        
class PV_Telegram_Parameter(Date_Format):
    def __init__(self):
        super().__init__()
        self.PV_Para = namedtuple('PV_Para', ['S1_V', 'S1_A', 'S1_W', 'S2_V', 'S2_A', 'S2_W', 'P1_V', 'P1_A','P2_V', 'P2_A','P3_V', 'P3_A', 'AC_Pt', 'DC_Pt','COS_p', 'TEMP', 'P_total'])
        self.l_dim = ('V','A','W','V','A','W','V','A','V','A','V','A','kWh AC','kWh DC','cosPh','°C', 'kWh ges')
        

class PV_Telegram(PV_Telegram_Parameter):
    def __init__(self):
        super().__init__()
        self.stat = 'Class initialized'
        
        
    #----------------    
    def get_Tele_Values(self, tel):
        self.stat_flag = True
        self.stat = 'ok'
        self.DateTime_str =''
        self.DateTime   = ""
        self.Date = ""
        self.Time = ""
        self.p = ""
        self.p_str =[]
        try:
            spindex = tel.find("*")
            #print(spindex)
            datetag = tel[0:spindex].strip()
            tele10 = ' '.join(tel[spindex:].split())
            tele11 = tele10.split(' ')
            l = tele11[4:-1]
            #print(l)
        except:    
            self.stat = 'falsches Telegram'
            if len(datetag) != 19:
                self.stat('falsches Datum-Format')
            self.stat_flag = False
            return
        self.DateTime_str = datetag.replace('-', '.')
        try:
            self.DateTime = self.str_to_date(self.DateTime_str)
            self.Date = self.DateTime.date()
            self.Time = self.DateTime.time()
        except:
            self.stat = 'falsches Datum Format'
            self.stat_flag = False
            return   
        self.p_dim = self.PV_Para._make(self.l_dim)
        #print(self.p_dim)
        if len(self.p_dim) != len(l): 
            self.stat = 'unterschiedliche Array länge'
            self.stat_flag = False
            return
        self.names  = self.PV_Para._fields
        # !! cos ph  c und i abfangen
        index = self.PV_Para._fields.index('COS_p')
        try:
            cos_f = float(l[index])
        except:
            l[index] = l[index][:-1] # letzten char löschen
        # array in float wandeln    
        try:
            l_double = np.array(l, dtype=np.float32)
            self.p = self.PV_Para._make(l_double)
            self.p = self.p._replace(P_total =self.p.P_total/1000)
            self.p = self.p._replace(AC_Pt =self.p.AC_Pt)
            self.p = self.p._replace(DC_Pt =self.p.DC_Pt/1000)
            for item in self.p:
                self.p_str.append("{:5.3f}".format(item))
            #print(self.p)    
        except:
            self.stat = 'falsche(r) Telegramwert'
            self.stat_flag = False
            return
#--End Class PV_Telegram-------------
       

       
             

class TagUtil():
    def __init__(self):
        self.total_power= 0.0

#---    
    def getFromTeleAllValues(self, t):
        tele = PV_Telegram()
        tele.get_Tele_Values(t)
        return tele   
            
#---            
    def getYearValues(self, year_Files):
        
        lk = list(year_Files.keys())
        lv = list(year_Files.values())
        root = lk[0]
        lastTeles = []
        yearYieldTotal = 0
        for item in lv[0]:
                pf = root + str(item)
                Teles = self.getAllTelegrammsInCSVFile(pf)
                lastTele = Teles[-1]
                #print(lastTele)
                dmTele = self.getFromTeleAllValues(lastTele)
                yearYieldTotal += dmTele.p.P_total
                
                lastTeles.append(dmTele)
           
        ListDMY, ytp = self.getDayMonthYearYield(lastTeles)
           
            
        tmp = str(ytp).replace('.', ',')
        ytpStr = re.sub(r'(?<!^)(?=(\d{3})+,)', r'.', tmp)
        return ListDMY, ytpStr
           
# ---        
    def getAllTelegrammsInCSVFile(self, fn):
        teles= []
        
        # get all telegrams in a file
        with open(fn, encoding="latin-1") as f:
              ls = f.readlines()
              for line in ls:
                  if len(line) > 100:
                      teles.append(line)
              return teles
    
 #---               
    def getAllDayTelegramms(self, pathFile, filter):
        
        # get all telegrams in a file
        teles = self.getAllTelegrammsInCSVFile(pathFile)
        #print(teles)   
        valuesTeleList =[]
        max_ACPower = 0
        count = 0
        for item in teles:
                  #print(item)
            try:
                  v = self.getFromTeleAllValues(item)
                  #print(v)
                  count +=1
                  #print(v.p)
                  #print(v.p.AC_Pt)
                  #print(v.p.TEMP)
                  #print(v.p.S1_W)
                  #print(v.p.S2_W)
                  #print(v.DateTime)
                  #print(v.stat)
                  valuesTeleList.append((v.DateTime, v.p.AC_Pt, v.p.TEMP, v.p.S1_W, v.p.S2_W))
                  if max_ACPower < v.p.AC_Pt:
                      max_ACPower = v.p.AC_Pt
                  if count == len(teles):
                      tpower = v.p.P_total
                      self.total_power = v.p.P_total                
            except:
                pass
        tpowerStr = str(tpower) + ' kWh'  
        #print(max_ACPower)
        max_ACPowerStr = str(max_ACPower /1000)
            
        A = [[],[],[],[],[]]
        count = 0
        #print(len(valuesTeleList))
        #print(filter)
        for item in valuesTeleList:
            if (count==0):
                A[0].append(item[0])
                A[1].append(item[1])
                A[2].append(item[2])
                A[3].append(item[3])
                A[4].append(item[4])
                #print(A[0])
                count +=1
            if(filter <= count):
                count = -1
            count +=1
        return A, tpowerStr, max_ACPowerStr
              #print(tpowerStr)
#---  
    def getAllLastTelegrams(self, dicMonthFiles):
        ut = Utils()
        lk = list(dicMonthFiles.keys())
        lv = list(dicMonthFiles.values())
        root = lk[0]
        
        lastTeles =[]
        for item in lv[0]:
            
            Teles = self.getAllTelegrammsInCSVFile(root+item)
            lastTele = Teles[-1]
            dmTele = self.getFromTeleAllValues(lastTele)
            #print(lastTele)
            lastTeles.append(dmTele)
        averagePower = 0
        totalPower = 0
        nrOfDay = 0
        for item in lastTeles:
                #print(lastTeles[index].p)
                totalPower += item.p.P_total
                averagePower += item.p.P_total 
                nrOfDay += 1
        averagePower = averagePower/ nrOfDay
            
        A =[[], [], []]
        for item in lastTeles:
                a1 = ut.getDateTimeZero(item.DateTime)
                A[0].append(a1)
                A[1].append(item.p.P_total)
                A[2].append(averagePower)
                   
        return A, totalPower
                       
            
#---
    def getMonthIndexYield(self, teles):
        monthIndexList = []
        for i in range(1, 13, 1):
            res = list(filter(lambda x: teles[x].Date.month == i , range(len(teles))))
            monthIndexList.append(res)  
        #print(monthIndexList)
        return monthIndexList
#---          
    def getDayMonthYearYield(self, lteles):
        ut = Utils()
        il = self.getMonthIndexYield(lteles)
        tpListTage = []
   
        tpListMonthYear =[]
        for i in range(1, 13, 1):
            tpListTage.append([0,0])
            tpListMonthYear.append([0,0])
        #print(tpListMonthYear)    
        #print(il)
        tpm = 0
        tpy = 0
        A =[[],[],[], [], []]
        '''
       
        A[0] month datetime
        A[1] month yield
        A[2] year average
        A[3] day date
        A[4] day power yield
        '''
        
     
     
        F3 = '{:06.3f}' 
        
        for indexes in il:
            if not not indexes:
                     #print(indexes[-1]) 
                     indexLastDayInMonth = indexes[-1]
                     for index in indexes:
                         A[3].append(lteles[index].Date)
                         A[4].append(lteles[index].p.P_total)
                         tpm = tpm + lteles[index].p.P_total
                     tpmF = float(F3.format(tpm))
                     A[1].append(tpmF)
                     tpy = tpy + tpm
                     dt = ut.getDateTimeZero(lteles[index].Date)
                     A[0].append(dt.replace(day=1))
                     tpm = 0
                     
        #print(A[0])                          
        #print(A[1])
        #print(A[2])
        #print(A[3])                                   
        #print(tpy)
        #print(month_data_availabe_count)
        
        tpystr = F3.format(tpy) # years yield
        #print(tpystr)   
        return A, tpystr





