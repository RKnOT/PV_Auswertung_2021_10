#!/usr/bin/env python3

import os

import sys
import math
from datetime import date, datetime, timedelta
import calendar

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.dates import DateFormatter

cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')
from CommonClasses.DataModel import TagUtil as TagRecord
from CommonClasses.DataModel import GetCSV_File_Names as GetCSV_Names
from helper_classes import check_CSV

# git test

#-------Eingabe-----------
DaySelected = 21

MonthSelected = 12
YearSelected = 2021
#------
TeleSelected = 0
#--------------------

'''
 TO DO: 
    ok. CHECK RANGE DAY / MONTH / YEAR 


p1 = os.getcwd()
print(p1)
os.chdir('..')
p1 = os.getcwd()
print(p1)
'''
DF3 ='%d. %B %Y'
F3 = '{:06.3f}'
DF_h_m_s = mdates.DateFormatter('%H.%M.%S')
DF_day_Month = DateFormatter('%d. %b')
DF_M = mdates.DateFormatter('%b')


   


#------------------
class YearView():
    def __init__(self, csv):
        #print(csv.status)
        #print(csv.selected_Year_Files)
        self.yv(csv)
        
    def yv(self, csv):
        dm = TagRecord()
        A, tpy = dm.getYearValues(csv.selected_Year_Files) 
        plotLines = [
                     [0, 'b2', 'blue', 1, '-', '', 20]
                    ]
        plotAchsBeschriftung= [
                               ['in kWh', 'black'],
                               ['', ''],
                               ['Monatsertrag in kWh'],
                               [DF_M],
                               ['Jahresertrag: '+ tpy+ ' kWh'],
                                'Jahr ' + str(A[0][0].year)
                              ]   
        i1 = []
        for i in A[1]:
           i1.append(math.ceil(i))
        A[1] = i1
        #print(A[1])
        Pd = PlotDiagram()
        #print(A[1])
        Pd.DV(A, plotLines, plotAchsBeschriftung)
#----------------------        
class MonthView():
    
    def __init__(self, csv):
        self.CSV = csv
        #print(csv.dic_year)
        self.mv(csv.selected_Month_Files)
        
    def mv(self, csv):
        dm = TagRecord() 
        A, monthYield = dm.getAllLastTelegrams(csv)
        #print(monthYield) 
        year = A[0][0].year
        month = A[0][0].month
        monthRange = calendar.monthrange(year, month)
        #print(monthRange)
        #print(A[0][-1].day)
        monthYield1 = A[2][0]*monthRange[1]
        monthYield1Str = F3.format(monthYield1)
        monthYieldStr = F3.format(monthYield)
        
        c0 = 'Tageserträge'+ ' im '+ A[0][0].strftime('%B %Y')
        c1 = "Monatsertrag:  "+ monthYieldStr + " kWh"

        if monthRange[1] != A[0][-1].day:
            c1 = "bisher "+ monthYieldStr + ' kWh'
            c1 += ' / hochgerechnet '+ monthYield1Str +' kWh'
        plotLines = [
                     [0, 'b1', 'blue', 1, '-', '', 0.8],
                     [1, 'p', 'red', 1, '-', 'kWh Ø']
                    ]
        plotAchsBeschriftung= [
                               ['in kWh', 'black'],
                               ['', ''],
                               [F3.format(A[2][0]) + ' kWh Ø','Ertrag / Tag'],
                               [DF_day_Month],
                               [c1],
                               c0
                              ]   
        Pd = PlotDiagram()
        Pd.DV(A, plotLines, plotAchsBeschriftung)
#----------------------               
class DayView():
   
    def __init__(self, csv):
        self.CSV = csv
        #print(csv.status)
        #print(csv.selected_Day_File)
        #print(csv.available_Years)
        self.dv(csv.selected_Day_File, TeleSelected)
        
    def dv(self, dayrecord, TeleSelected):
        dm =TagRecord()
        A, tpowerStr, max_ACPower= dm.getAllDayTelegramms(dayrecord, TeleSelected) 
        Pd = PlotDiagram()
        title = ('PV Tagesertrag ' + tpowerStr+ ' /  max AC Power ' + max_ACPower +' kWh')
        xAchseBeschr = 'am ' + A[0][0].strftime(DF3)
        plotLines = [
                         [0, 'p','blue', 1, '-', 'AC Power'], 
                         [1, 'p2', 'green', 0.5, ':', 'Temperatur'], 
                         [2, 'p', 'red', 1, '-', 'DC Power S1'],
                         [3, 'p', 'pink', 1, '-', 'DC Power S2'],
                        ]
        plotAchsBeschriftung= [
                                   ['in Wh', 'blue'], # ylabel left
                                   ['°C', 'green'], # ylabel right
                                   [''], # legend eine Achse
                                   [DF_h_m_s], # x Achse beschriftung
                                   [title], # titel
                                   xAchseBeschr
                                  ]
        Pd.DV(A, plotLines, plotAchsBeschriftung)
#-------------------------
class PlotDiagram():
    
    def DV(self, Lists, line, achs):
        
        #print(Lists[0])
        x = Lists[0]
        
        y =[]
        for i in range(1, len(Lists)):
             yt = []
             for item in Lists[i]:
                yt.append(item)
             y.append(yt)   
                
                
       
        #x_fmt = mdates.DateFormatter('%H.%M.%S')
        self.plot(x, y, line, achs)

    def plot(self, x, y, o, a): 
        def autolabel(rects):
           
    # Attach a text label above each bar in *rects*, displaying its height.
                
            for rect in rects:
                height = rect.get_height()
                ax1.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


       
           
        
        fig, ax1 = plt.subplots()
        ax1.set_title(a[4][0])
        ax1.set_ylabel(a[0][0], color = a[0][1])
           
                    
        ax2 = 0
        for item in o:
            #print(item)    
           
            if(item[1]== 'p'):
                ax1.plot(x, y[item[0]], color= item[2], label = item[5], linewidth = item[3], linestyle= item[4])
            if(item[1]== 'p2'):
                if(ax2 == 0):
                    ax2 = ax1.twinx()
                ax2.plot(x, y[item[0]], color = item[2], label = item[5], linewidth = item[3], linestyle= item[4])
            if(item[1][0]== 'b'):
                r1 = ax1.bar(x, y[item[0]], color= item[2],linewidth=item[3], width= item[6], align='center')
                if(item[1][1]== '2'):
                   autolabel(r1)
        ax1.set_xlabel(a[5]) 
        if(ax2 != 0):
            # Zwei y Achsen Legende zusammenfassen
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc=0)
           
            ax2.set_ylabel(a[1][0], color =a[1][1])
            
            ax2.xaxis.set_major_formatter(a[3][0])
        ax1.grid(True)
        fig.autofmt_xdate()    
        if(ax2==0):
            plt.legend(a[2])
            ax1.xaxis.set_major_formatter(a[3][0]) 
            ax1.xaxis_date()
            #ax1.set_xlabel('hjhjh')
        plt.show()
        plt.close()      
      


if __name__ == '__main__':
        c = check_CSV(DaySelected, MonthSelected, YearSelected)
        #_ = os.system('clear')
   
        if c.csv.day_record_flag:
           DayView(c.csv)
          
           pass
        if c.csv.month_record_flag:
           MonthView(c.csv)
           pass
        
        if c.csv.year_record_flag:   
           YearView(c.csv)
           pass

    


