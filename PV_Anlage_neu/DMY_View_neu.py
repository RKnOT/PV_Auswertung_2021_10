#!/usr/bin/env python3

import os
import csv
import sys
import json
import pathlib


from datetime import datetime
'''
import math
from datetime import date, datetime, timedelta
import calendar

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.dates import DateFormatter
'''
cwd = os.getcwd()

#print(cwd)
csv_dir = cwd + '/PVDataLog'
sys.path.insert(1, cwd + '/CommonClasses')
#from CommonClasses.DataModel import TagUtil as TagRecord
#from CommonClasses.DataModel import GetCSV_File_Names as GetCSV_Names

#import Dir_File_Handling
#from helper_classes import check_CSV

#-------Eingabe-----------
DaySelected = 3
MonthSelected = 8
YearSelected = 2023
#------
TeleSelected = 0
#--------------------

#--------------
#csv_obj = GetCSV_Names(cwd + '/PVDataLog', '2023_07', 'csv')
class CSV_file_handling():
	def __init__(self, csv_dir_path, ext = 'CSV'):
		self.Ext = ext
		self.cwd = os.getcwd()
		self.Path_csv = self.cwd + '/' + csv_dir_path
		self.List_csv_files = []
		self.list_csv_file_content = []
		self.dic_days = {}
		
		self.get_all_csv_files()
		
	def get_all_csv_files(self):
		os.chdir(self.Path_csv)
		for fn in os.listdir('.'):
			ext_file = pathlib.Path(self.Path_csv + '/' + fn).suffix
			if ext_file == '.' + self.Ext:
				self.List_csv_files.append(fn)
		os.chdir(self.cwd)
		return
	
	def get_csv_data(self, f_name):
		os.chdir(self.Path_csv)
		list_day_items = [[], []]
		with open(f_name) as csv_file:
			reader = csv.reader(csv_file)
			line_count = 0
			day_count = 0;
			for row in reader: # get item header
				if line_count == 0:
					str_header = " , " . join(row)
					self.l_header = str_header.split(';')
					self.l_header.pop(0)
					line_count += 1
				else:						# get item content
						str_items = ' , ' . join(row)
						items = str_items.split(';')
						items.pop(0)
						self.list_csv_file_content.append(items)
						if items[0][:10] not in list_day_items[0]:
							list_day_items[0].append(items[0][:10])
							list_day_items[1].append(line_count-1)
						line_count += 1
			for day_element in list_day_items[0]: 
				start_index = list_day_items[1][day_count]
				
				if day_count >= len(list_day_items[0])-1:
					stop_index = line_count - 1
				else:
					stop_index = list_day_items[1][day_count+1]
				self.dic_days[str(day_count)] = [day_element, start_index, stop_index]
				day_count +=1
			#print(self.dic_days)
			os.chdir(self.cwd)
			
	def get_dic_header(self, l_header):
		i = 0
		temp_str = '{'
		for item in l_header:
			temp_str += '"' + str(i) + '" : ' + '"' + item + '",'
			i +=1
		temp_str = temp_str[:-1]	
		temp_str += '}'
		#print(temp_str)
		self.h_dict = json.loads(temp_str)
		
#-----class end----------		
class get_days_month_year_views():
		def __init__(self, sub_dir = 'PVDataLog', ex= 'csv'):
			all_csv = CSV_file_handling(sub_dir, ex)
			list_months_days = []				
			#read all csv's
			for item in all_csv.List_csv_files:
			
				#list_months_days.append(all_csv.days_view)				
				all_csv.get_csv_data(item)
				list_months_days.append()
				all_csv.get_dic_header(all_csv.l_header)
				tele = csv_content_handling(all_csv.list_csv_file_content, all_csv.dic_days)			
			
			print(list_months_days)
#-------------		
class csv_content_handling():
	def __init__(self, list_csv_content, dic_days):
		self.list_csv_content = list_csv_content
		self.dic_days = dic_days
		self.days_view = []
		self.month_view =[]
		self.get_days_month_view()
	
	def get_days_month_view(self):
		for i in range(0, len(self.dic_days)):
			start_index = self.dic_days[str(i)][1]
			stop_index = self.dic_days[str(i)][2]		
			record_values = self.convert_content_items_to_values(self.list_csv_content[0])
			#print(record_values)
			list_day_temp = [0] * len(record_values[1:])
			list_month_temp = [0] * len(record_values[1:])
			# get days view	
			for j in range(start_index, stop_index):
				record_values = self.convert_content_items_to_values(self.list_csv_content[j])
				rv_date = record_values[0].date()
				record_values  = record_values[1:] 
				for index, integer in enumerate(record_values):
   				 list_day_temp[index] += integer
			list_day_temp.insert(0, rv_date)
			self.days_view.append(list_day_temp)
		# get month view
		self.month_view =self.add_list_items_values(self.days_view)
		print(self.month_view)
			
	def add_list_items_values(self, list_values):
		list_temp = [0] * len(list_values[0][1:])
		
		for item in list_values:
			date = item[0]
			
			for index, value in enumerate(item[1:]):
				list_temp[index] += value
		list_temp.insert(0, date)
		return list_temp	
									
	def convert_content_items_to_values(self, data_set):
		date_format = '%Y-%m-%d %H:%M:%S'
		flag_first_item = True
		list_data_set_values = []
		for item in data_set:
			if flag_first_item:
				item = item + ':00'
				date_obj = datetime.strptime(item, date_format)
				list_data_set_values.append(date_obj)
			else:
				list_data_set_values.append(int(item))
			flag_first_item = False
		return list_data_set_values
			
#----- end class
		
				
get_days_month_year_views()


#print(all_csv.l_header[0])

#print(all_csv.list_csv_file_content[0])
#print()

'''
start_index = all_csv.dic_days['29'][1]
stop_index = all_csv.dic_days['29'][2]
for i in range(start_index, stop_index):
	print(all_csv.list_csv_file_content[i])
'''
	
		
#tele = csv_content_handling(all_csv.list_csv_file_content, all_csv.dic_days)			


#print(all_csv.h_dict)
#for item in tele.days_view:
	#print(item)
					
	
#print(all_csv.dic_days)

#print(all_csv.list_csv_file_content[all_csv.list_day_items[1][1]-1])


#print(type(all_csv.h_dict))
#print(len(all_csv.h_dict))



#for i in all_csv.h_dict:
	#print(all_csv.h_dict[str(i)])
	
	
	

'''


 TO DO: 
    ok. CHECK RANGE DAY / MONTH / YEAR 


p1 = os.getcwd()
print(p1)
os.chdir('..')
p1 = os.getcwd()
print(p1)

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
                               ['Jahresertrag: '+ tpy + ' kWh'],
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
        #print(csv)
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
        #print(dir(dm))
        A, tpowerStr, max_ACPower= dm.getAllDayTelegramms(dayrecord, TeleSelected) 
        Pd = PlotDiagram()
        title = ('PV Tagesertrag ' + tpowerStr+ ' /  max AC Power ' + max_ACPower +' kWp')
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
                # check if only one day or month is available 
                delta_time = timedelta(days = 0)
                if len(x) == 1:
                    delta_time += timedelta(days = 1)
                ax1.set_xlim(x[0], x[-1] + delta_time)
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
            pass
        
        plt.show()
        plt.close()
        
        
        
        
       
        
        import numpy as np

        x = np.arange(0, 12)
        y = np.arange(20, 32)
        
        month_xticks = ['Jan','Feb','März','April','Mai','Juni','Juli', 'Aug', 'Sep','Okt', 'Nov', 'Dez']
        
        
        print(x)
        print(y)
        
        plt.xticks(x, month_xticks)
        plt.plot(x, y)
        plt.show()      
        

if __name__ == '__main__':
        c = check_CSV(DaySelected, MonthSelected, YearSelected)
        _ = os.system('clear')
   
        if c.csv.day_record_flag:
           DayView(c.csv)
           pass
        if c.csv.month_record_flag:
           MonthView(c.csv)
           pass
        
        if c.csv.year_record_flag:   
           YearView(c.csv)
           pass

'''    


