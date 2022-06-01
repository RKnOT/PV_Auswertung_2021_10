import matplotlib.pyplot as plt




import numpy as np

import json
import os
import sys
from datetime import datetime
import UtilsClasses as ut



from DataModel import GetCSV_File_Names as GetCSV_Names

#from DataModel import TagUtil as TagRecord


fpath = '/private/var/mobile/Containers/Shared/AppGroup/FA16265D-A93E-42FB-9932-E3CC306D50A8/File Provider Storage/Repositories/Python_Utils/Date_Time_Utils'
sys.path.append(fpath)

fpath = '/private/var/mobile/Containers/Shared/AppGroup/FA16265D-A93E-42FB-9932-E3CC306D50A8/File Provider Storage/Repositories/Python_Utils/PV_Utils'
sys.path.append(fpath)

fpath = '/private/var/mobile/Containers/Shared/AppGroup/FA16265D-A93E-42FB-9932-E3CC306D50A8/File Provider Storage/Repositories/Python_Utils/PY_snippes'
sys.path.append(fpath)

import date_time_util as dtu
import PV_Helper_Utils as hpu
import Color_Map as cm

#print(sys.path[0])


	
		
#--- debug helpers_date_handling ----------

#test_date = '2021_12_22'
#test_date = '2021_12_22 23:12:00'
#hp1 = dtu.helpers_date_handling(test_date, debug_flag = True)
#hp2 = dtu.helpers_date_handling(debug_flag = True)
#diff = hp1.date_time_differenz(hp2 , hp1)
#print(diff)

#___________________________________________

def compare_date_now_and_recorted():
	flag_same_date = False
	hp = hpu.helpers()
	dt_recorted = list(hp.readJsonFile(agr.dir_file_dic['last_recorded_date']).values())
	#print(dt_recorted)
	dt_rc = dtu.helpers_date_handling(dt_recorted[0])
	dt_now = dtu.helpers_date_handling()	
	
	time_dic = dt_rc.date_time_differenz(dt_rc, dt_now)
	
	if time_dic['same_year_month_day_flag']:
			flag_same_date = True 
	print(dt_rc.datum_dic['date_date'])
	print(dt_now.datum_dic['date_date'])
	print(time_dic['same_date_flag']) #== False:
	
	
if __name__ == '__main__':
		
		Show_Charts = 1
		
		# debug
		#print(helpers_date_handling.__init__.__doc__)
		
		hp = hpu.helpers()
		agr = hpu.Aggregate_Years_CSV()
		
		compare_date_now_and_recorted()
		
		
		
		#print(agr.dir_file_dic)
		recorted_date_time = ''
		
		current_year_str = hp.datum_dic['year_str']
		current_date_time = hp.datum_dic['date_time_str']
		current_date_time_record = {'Date_Time_recorted' : hp.datum_dic['date_time_str']}
		
		years_yields = ''
		year_yield = ''
		json_write = ''
		
		# check last date record
		#print(agr.dir_file_date)
		content = hp.readJsonFile(agr.dir_file_dic['last_recorded_date'])
		#print(content)
		if content == {}:
			print('no date file available')
			#read all years yields
			years_month_yield_dic = agr.aggregate_yield()
			#print(years_yield)
		else: 
			recorted_date_time = list(content.values())[0]
			years_month_yield_dic = hp.readJsonFile(agr.dir_file_dic['years_month_yield_data'])
			#print(list(content.keys())[0])
			#print(hp.datum_dic)
			#print(hp.datum_dic['date_str'])
			pass
		
		#------------------------	
		
		if Show_Charts == 1 or Show_Charts == 10:
			
			#print(years_month_yield_dic)		
			#print('current date time: ', current_date_time)
			#print(hp.datum_dic['date_time_str'])
			#print('recorted date time: ', recorted_date_time)
			hp_date_rec = dtu.helpers_date_handling(recorted_date_time)
			time_dic = hp_date_rec.date_time_differenz(hp, hp_date_rec)
			if time_dic['same_date_flag'] == False:
				#print(list(content.values())[0])
				#print(current_year_str)
				year_yield = agr.aggregate_yield([hp.datum_dic['year_str']])
					
			if year_yield != '':
				# update current year yields from files
				years_month_yield_dic[current_year_str] = year_yield[current_year_str]	
			#print(years_month_yield_dic)
			#print(years_month_yield_dic.keys())
			years_month_yield_aufgezeichnet = hp.readJsonFile(agr.dir_file_dic['years_month_yield_data'])
			#print(years_month_yield_aufgezeichnet)
			#print(hp.years_month_yield(years_month_yield_aufgezeichnet))
			#print(hp.years_yield_abgerechnet_dic())
		
			years_yield_aufgezeichnet = hp.years_month_yield(years_month_yield_aufgezeichnet)

			years_yield_abgerechnet = hp.years_yield_abgerechnet_dic()
			#print(years_yield_abgerechnet)
		
			# write current date to json
			#--------------------lölölölölölöl
			hp.writeJsonFile(agr.dir_file_dic['last_recorded_date'], current_date_time_record) 
			# write current years month yield to json
			hp.writeJsonFile(agr.dir_file_dic['years_month_yield_data'], years_month_yield_dic) 
		
			# write years yield aufgezeichnet to json
			hp.writeJsonFile(agr.dir_file_dic['years_yield_data_aufgezeichnet'], years_yield_aufgezeichnet) 
			# write years yield abgerechnet to json
			hp.writeJsonFile(agr.dir_file_dic['years_yield_data_abgerechnet'], years_yield_abgerechnet) 
		
			# plot graph
			pl = hp.convert_to_bar_plot_lists(years_yield_abgerechnet, years_yield_aufgezeichnet)
			#print(pl.keys())
			# dict_keys(['x_bezeichnung', 'x_werte', 'y_werte_liste'])
		
			# Declaring the figure or the plot (y, x) or (width, height)
			plt.figure(figsize=[15, 10])
			# Data to be plotted
			# Passing the parameters to the bar function, this is the main function which creates the bar plot
			# Using X now to align the bars side by side
			color = ['g', 'y', 'r', 'pink']
			ind = 0
			w = 0.
			ws = 0.1
			for yn in pl['y_werte_liste']:
				plt.bar(pl['x_werte'] + (w), yn, color = color[ind], width = ws)
				ind += 1
				cl = len(color)
				if ind % cl == 0:
					ind = 0
				w += ws
			# Creating the legend of the bars in the plot
			plt.legend(['Abgerechnet', 'Ermittelt'])
			# Overiding the x axis with the country names
			plt.xticks([i + ws for i in range(len(pl['x_bezeichnung']))], pl['x_bezeichnung'])
			# Giving the tilte for the plot
			plt.title("Jahres Erträge Abgerechnet / Ermittelt")
			# Namimg the x and y axis
			plt.xlabel('Jahre')
			plt.ylabel('kWh')
			# Saving the plot as a 'png'
			#plt.savefig('4BarPlot.png')
			# Displaying the bar plot
			plt.show()
		
#------------------------
		if Show_Charts == 2 or Show_Charts == 10:
			
			yma = hpu.Get_years_month_average()
			years = list(yma.y_m_av_dic.keys())
			pos = np.arange(len(years))
			l_plot_month = 1
			l_plot_value = []
			flag_one = True
			for i in years:
				m_keys = list(yma.y_m_av_dic[i].keys())
				m_values = list(yma.y_m_av_dic[i].values())
				#print(m_keys)
				#print(m_values)
				m_key = list(map(lambda x : x, m_keys))
				m_value = list(map(lambda x : x[1], m_values))
				if flag_one:
					l_plot_month = m_key
					flag_one = False
				l_plot_value.append(m_value)
			
			color = cm.color_map()[10:]
			plt.figure(figsize=[15, 10])
			
			pos = np.arange(len(l_plot_month))
			w = 0.
			ws = 0.1
			#print(pos)
			ci = 0
			for i in l_plot_value:
				#print(i)
				plt.bar(pos+w, i, color= color[ci], edgecolor='black', width = ws)
				
				w += ws
				ci +=2
				if ci % len(color) == 0:
					ci = 0
			plt.xticks(pos, l_plot_month)
			#plt.xticks(rotation = 45)
			#plt.setp(xaxis.get_majorticklabels(), ha='right')
			plt.xlabel('Monat', fontsize=16)
			plt.ylabel('Durchschnittlicher Tages-Ertrag in kWh', fontsize=16)
			plt.title('Tages-Ertrag im Durchschnitt',fontsize=18)
			plt.legend(years,loc=2)
			plt.show()
			
			
			
			
			
		#------------------------
		
		
		
	
