#!/usr/bin/env python3

import os
import csv
import re
import math
from datetime import date, datetime, timedelta

import calendar

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.dates import DateFormatter

# String- / Float-Formate 
DF1 = '%d.%m.%Y %H:%M:%S'

DF2 ='%d. %b %Y'
DF3 ='%d. %B %Y'

DF4 = '%d.%b'
DF5 = '%H.%M.%S'
DF6 ='%b %y'

DF_day_Month = DateFormatter('%d. %b')
DF_h_m_s = mdates.DateFormatter('%H.%M.%S')
DF_M = mdates.DateFormatter('%b')

F1 = '{:07.3f}'
F2 = '{:05.3f}'
F3 = '{:06.3f}'


#------------------
class Plot_day_view():
    def __init__(self, v):
        Pd = PlotDiagram()
        title = ('PV Tagesertrag ' + v.tpowerStr+ ' /  max AC Power ' + v.max_ACPower +' kWh')
        xAchseBeschr = 'am ' + v.A[0][0].strftime(DF3)
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
        Pd.DV(v.A, plotLines, plotAchsBeschriftung)
#------------
    












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
               
            if(item[1][0]== 'b'): 
                r1 = ax1.bar(x, y[item[0]], color= item[2], label = item[5], linewidth = item[3], linestyle= item[4], align ='center', width = item[6])         
                if(item[1][1]== '2'):
                   
                    autolabel(r1)
            
            if(item[1]== 'p2'):
                if(ax2 == 0):
                    ax2 = ax1.twinx()
                ax2.plot(x, y[item[0]], color = item[2], label = item[5], linewidth = item[3], linestyle= item[4]) 
       
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
      

#------------------