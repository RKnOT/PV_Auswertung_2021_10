import matplotlib.pyplot as plt
import numpy as np

import json
import os
import datetime

import UtilsClasses as ut


from DataModel import GetCSV_File_Names as GetCSV_Names

from DataModel import GetCSV_File_Names as PV_Telegram
from DataModel import TagUtil as TagRecord

#------------------------------------
class helpers_date_handling():
	def __init__(self, debug = False):
		'''
-- helpers_date_handling class --		
Doc Aufruf: 
	print(helpers_date_handling.__init__.__doc__)
Dictionary with the following current date keyes:
	dict_keys(['year_str', 'year_int', 'month_str', 'month_int', 'day_str', 'day_int', 'date_str', 'date_datetime'])
add days:
	t1 = self.datum_dic['current_date_datetime']
	t2 = t1 + datetime.timedelta(days=2)
	print(t2)
		
		'''
		self.get_current_date()
		if debug:
			print(self.datum_dic)
			print(self.datum_dic.keys())
	
	def get_current_date(self):
		self.datum_dic = {}
		now = datetime.datetime.now()
		self.datum_dic['year_str'] = now.strftime('%Y')
		self.datum_dic['year_int'] = int(self.datum_dic['year_str'])
		self.datum_dic['month_str'] = now.strftime('%m')
		self.datum_dic['month_int'] = int(self.datum_dic['month_str'])
		self.datum_dic['day_str'] = (now.strftime('%d'))
		self.datum_dic['day_int'] = int(self.datum_dic['day_str'])
		self.datum_dic['date_str'] = self.datum_dic['day_str'] + '_' + self.datum_dic['month_str'] + '_' + self.datum_dic['year_str']
		self.datum_dic['date_datetime'] = datetime.datetime.strptime(self.datum_dic['date_str'], '%d_%m_%Y').date()
		
	
		

class helpers(helpers_date_handling):
	
	def __init__(self):
			super().__init__()
	
	'---------------'
	def gen_empty_year_month_yield(self): 
		year_month_empty_dic = {}
		for i in range(1, 13):
			m = f'{i:02d}'
			year_month_empty_dic[m] = 0.0
		return year_month_empty_dic
			
	'--------------'
	def gen_years_yield_empty(self, start_year = 2012):
		years_empty_dic = {}
		now = datetime.datetime.now()
		current_year = int(now.strftime("%Y"))
		current_year = current_year			
		year_count = current_year - start_year
		for i in range(2012, current_year):
			years_empty_dic[str(i)] = 0
		return years_empty_dic
	'----------------'	
	def years_yield_abgerechnet_dic(self):
		 year_yield_abgerechnet_dic = {'2012': 431.0, '2013': 7325.0, '2014': 7878.0, '2015': 7733.0, '2016': 7729.0, '2017': 7797.0, '2018': 7972.0, '2019': 7644.0, '2020': 7301.0, '2021': 6705.0, '2022': 0.0}
		 return year_yield_abgerechnet_dic
	'----------------'
	def years_month_yield(self):
		years_month_yield_dic = {'2012': {'01': 0.0, '02': 0.0, '03': 0.0, '04': 0.0, '05': 0.0, '06': 0.0, '07': 0.0, '08': 0.0, '09': 0.0, '10': 134.47799999999998, '11': 208.01399999999995, '12': 105.84400000000002}, '2013': {'01': 103.91399999999999, '02': 198.77499999999998, '03': 566.99299999999982, '04': 772.45999999999992, '05': 972.08600000000001, '06': 1117.6950000000002, '07': 1410.3979999999997, '08': 1153.4420000000002, '09': 660.8850000000001, '10': 435.38700000000017, '11': 186.82699999999997, '12': 191.74200000000002}, '2014': {'01': 206.75899999999999, '02': 399.04599999999994, '03': 792.1350000000001, '04': 838.55600000000004, '05': 1087.1199999999999, '06': 1375.8909999999998, '07': 993.85299999999984, '08': 910.68700000000013, '09': 709.94499999999994, '10': 482.65800000000002, '11': 191.46199999999999, '12': 116.79300000000001}, '2015': {'01': 147.99200000000002, '02': 236.47200000000004, '03': 754.86900000000014, '04': 387.44400000000007, '05': 983.84000000000003, '06': 1201.2860000000001, '07': 1322.0159999999998, '08': 1112.1320000000001, '09': 758.10000000000002, '10': 436.71399999999988, '11': 219.62800000000004, '12': 173.02500000000001}, '2020': {'01': 0.0, '02': 0.0, '03': 0.0, '04': 264.25099999999998, '05': 1059.7780000000002, '06': 890.39499999999987, '07': 1133.665, '08': 872.91399999999976, '09': 667.8420000000001, '10': 346.84800000000007, '11': 185.85499999999999, '12': 70.75200000000001}, '2021': {'01': 28.644999999999996, '02': 294.35599999999994, '03': 659.23099999999988, '04': 897.67400000000009, '05': 908.54700000000037, '06': 1101.683, '07': 921.1869999999999, '08': 763.33100000000002, '09': 746.71199999999999, '10': 415.58099999999996, '11': 153.73000000000005, '12': 110.48099999999999}, '2022': {'01': 209.87899999999999, '02': 368.44100000000003, '03': 748.68799999999999, '04': 620.09499999999991, '05': 0.0, '06': 0.0, '07': 0.0, '08': 0.0, '09': 0.0, '10': 0.0, '11': 0.0, '12': 0.0}}
		
		years_yield_dic = self.gen_years_yield_empty()
		for k in list(years_month_yield_dic.keys()):
			#print(k)
			year_yield = 0.0
			for k1 in years_month_yield_dic[k]:
				month_yield_format = "{:8.3f}".format(years_month_yield_dic[k][k1])
				#print("year {}: | month : {} | yield : {}".format(k, k1, month_yield_format))
				year_yield += years_month_yield_dic[k][k1]
			years_yield_dic[k] = year_yield 
		#print('----')	
		#print(years_yield_dic)
		return years_month_yield_dic, years_yield_dic
	'-----'
	def convert_to_plot_list(self, dic_list):
		x = []
		y = []
		for k in list(dic_list.keys()):
			x.append(int(k))
			y.append(dic_list[k])
		return x, y		
	
	'------'
	def writeJsonFile(self, dest_file_name, file_content):
		with open(dest_file_name, 'w') as outfile:
			json.dump(file_content, outfile)
			pass
	
	def readJsonFile(self, dest_file_name):  
		if os.path.exists(dest_file_name):
			with open(dest_file_name) as json_file:
				data = json.load(json_file)
		else: 
			data = {}	
		return data
		
#------------------------------------


class Aggregate_Years_CSV():
	def __init__(self):
		
		self.helpers = helpers()
		self.nwd = ut.NetworkData()
		self.nwd.iniData()
		
		self.last_entry_dic = {}
		dir_aggr = 'Aggregation'
		last_record_date_json_file_name = 'last_recorded_date.json'
		years_yield_data_json_file_name = 'years_yield_data.json'
		
		#-------------- check year dir exists locally------
		dest = self.nwd.dir_local_CSV + '/' + dir_aggr + '/'
		if os.path.isdir(dest) == False:
			os.mkdir(dest)
		#---------------------------------------------------
		self.dir_file_date = dest + last_record_date_json_file_name
		
		self.dir_file_recorded_data = dest + years_yield_data_json_file_name
		
		
	
	def check_dirs_exists(self):
		year_file_names = {}
		
		year_month_names = {}
		list_temp = []
		key_years = list(self.dic_y_m_d.keys())
		for key_year in key_years[0:-1]: # without aggregation dir
			list_temp.append(key_year + '.json')
			month = list(self.dic_y_m_d[key_year].keys())
			list_month = []
			for key_month in month:
				list_month.append(key_year +'_'+ key_month+ '.json""')
			year_month_names[key_year] = list_month
		year_file_names['Years'] = list_temp		
				
		print((year_file_names['Years']))
		print(year_month_names)		
		
		
		for item in year_file_names['Years']:
			dest = self.dest + item
			#print(dest)
			# Writing to sample.json
			#self.writeJsonFile(dest, dictionary)
			#break		
		pass
	
	
	def aggregate_yield(self, years_selected = ['']):  
			
		I_get_csv_file_names = ut.Get_CSV_File_Names_from_Dir(years_selected)
		
		self.dic_y_m_d = I_get_csv_file_names.years_month_days_dic
		'''
		print('----')
		print(self.dic_y_m_d)
		print('----')
		'''
		month_monthYield_dic = {}
		dm = TagRecord()
		list_day_yield_pro_month = []
		years_month_yields = {}
		key_years = list(self.dic_y_m_d.keys())
		#print(key_years)
		
		year_month_yield_dic = {}
		month_1_12 = self.helpers.gen_empty_year_month_yield()
		for key_year in key_years:
			# debug
			#if key_year == '2014': break
			#------------
			print(key_year)
			month = list(self.dic_y_m_d[key_year].keys())
			for key_month in month:
				
				month_yield = 0.0
				dic_month = {}
				list_days_in_month = []
					
				days_in_month = self.dic_y_m_d[key_year][key_month]
				for i3 in days_in_month:
					file_name = key_year +'_'+ key_month +'_'+ i3
					gcsvN = GetCSV_Names(self.nwd.dir_local_CSV, file_name)
					list_days_in_month.append(key_year +'_'+ key_month + '_'+ i3 + '.CSV')
				dic_month[gcsvN.path] = list_days_in_month
				#print(dic_month)
				dm = TagRecord()
				A, monthYield = dm.getAllLastTelegrams(dic_month)
				
				month_1_12[key_month] = monthYield 
			#print('---')
			year_month_yield_dic[key_year] = month_1_12
			month_1_12 = self.helpers.gen_empty_year_month_yield()
		#print(month_1_12)
		#print(year_month_yield_dic)
		return year_month_yield_dic
		
	
		
		'''
		for item in list_file_names:
			gcsvN = GetCSV_Names(nwd.dir_local_CSV, item)
			dm =TagRecord()
			A, tpowerStr, max_ACPower= dm.getAllDayTelegramms(gcsvN.selected_Day_File, 0) 
			print(dm.total_power, max_ACPower)
			#day_tele = PV_Telegram()
			#print(gcsvN.dic_year)
			#print(gcsvN.selected_Year_Files)
			
			#print(gcsvN.selected_Day_File)
			#return
			pass
		'''

if __name__ == '__main__':
		
		# debug
		#print(helpers_date_handling.__init__.__doc__)
		
		hp = helpers()
		agr = Aggregate_Years_CSV()
		
		current_year_str = hp.datum_dic['date_str']
		current_date = {current_year_str : 'ok'}
		
		years_yields = ''
		year_yield = ''
		json_write = ''
		# check last date record
		content = hp.readJsonFile(agr.dir_file_date)
		if content == {}:
			print('no date file available')
			#read all years yields
			years_yield = agr.aggregate_yield()
		else: 
			#print(list(content.keys())[0])
			#print(hp.datum_dic['date_str'])
			pass
			
		if list(content.keys())[0] != hp.datum_dic['date_str']:
			year_yield = agr.aggregate_yield([hp.datum_dic['year_str']])
					
		years_yield = hp.readJsonFile(agr.dir_file_recorded_data)
		
			
		if year_yield != '':
			years_yield[hp.datum_dic['year_str']] = year_yield
			pass	
		
		all_years_list = ['']
		
		
		print(years_yield)
		
		
		hp.writeJsonFile(agr.dir_file_recorded_data, years_yield)
		hp.writeJsonFile(agr.dir_file_date, current_date) # write current date to json
		
		
		
		
		
		
		
		#agr.aggregate_yield([current_year_str])
		
		
		
		
		#last_date = list(hp.readJsonFile(agr.dir_file_date).keys())[0]
		#print(last_date)	
		
		
		'''
		year_empty_dic = hp.gen_years_yield_empty()
		#print(year_empty_dic)
		years_yield_abgerechnet = hp.years_yield_abgerechnet_dic()
		
		years_month, years_yield_aufgezeichnet  = hp.years_month_yield()
		
		print(agr.years_aggregation[current_year_str])
		print('----')
		print(years_month[current_year_str])
		
		if agr.years_aggregation[current_year_str] == years_month[current_year_str]:
			print(True)
		else:
			print(False)
		
		years_month[current_year_str] = agr.years_aggregation[current_year_str]
		
		if agr.years_aggregation['2022'] == years_month['2022']:
			print(True)
		else:
			print(False)
		
		print('----')
		print(years_month)
		hp.writeJsonFile(des_file_years_yield, years_month)
		
		
		
		
		#print(years_yield_aufgezeichnet)
		#print('---')
		#print(years_yield_abgerechnet)
		x1, y1 = hp.convert_to_plot_list(years_yield_abgerechnet)
		x2, y2 = hp.convert_to_plot_list(years_yield_aufgezeichnet)
		#print(x1)
		print(y1)
		#print(x2)
		print(y2)
		
		
		
		# Declaring the figure or the plot (y, x) or (width, height)
		plt.figure(figsize=[15, 10])
		# Data to be plotted
		X = np.arange(len(x1))
		
		# Passing the parameters to the bar function, this is the main function which creates the bar plot
		# Using X now to align the bars side by side
		plt.bar(X, y1, color = 'black', width = 0.25)
		plt.bar(X + 0.25, y2, color = 'g', width = 0.25)
		# Creating the legend of the bars in the plot
		plt.legend(['Abgerechnet', 'Ermittelt'])
		# Overiding the x axis with the country names
		plt.xticks([i + 0.25 for i in range(len(x1))], x1)
		# Giving the tilte for the plot
		plt.title("Jahres Erträge Abgerechnet / Ermittelt")
		# Namimg the x and y axis
		plt.xlabel('Jahre')
		plt.ylabel('kWh')
		# Saving the plot as a 'png'
		#plt.savefig('4BarPlot.png')
		# Displaying the bar plot
		plt.show()
		
		
		
		
		
		
		
		
				
		mul = lambda x: (lambda y: y * x)
		times4 = mul(4)
		print(times4(2))
		
		
		def str_handling(x):
			#ml = list(map(lambda y: x[0:10] if x[4:8] == y else '', m_list))
		
			ml = list(map(lambda y: x[8:10] if x[4:8] == y else '', m_list))
			mx = list(filter(lambda x: x if x != '' else '', ml ))
			
			return mx
		
		af = list(map(lambda x: str_handling(x), list_fn))
		print(af)
		
		
		def check_month():
			test = lambda x,y : y if y[4:8] == x else '-'
			if test != '-': 
				return test
		
		check = check_month()
		for item in m_list:
			for item_02 in list_fn:
				temp = check(item, item_02)
				
				if temp != '-': print(temp)
		
		#num = (lambda x: "one" if x == 1 else( "two" if x == 2 else ("three" if x == 3 else "ten")))(3)
		#print(num)
		
		#p1 = (lambda x: x[0:10] if x[4:8] == '_01_' else('twoooo'))('2022_01_07.CSV')
		#print(p1)
		
		
		p2 = list(map(lambda x: x[0:10] if x[4:8] == '_01_' else '' , list_fn))
		print(p2)
		
		p3 = list(map(lambda x: x[0:10] if x[4:8] == '_01_' else '' , list_fn))
		print(p3)
		
		
		from functools import partial  
		add = lambda x, y: x + y  
		inc = partial (add, 1)  
		map = lambda f, l: [f(x) for x in l]  

		s = [0, 1, 2, 3]  
		s_nested = [s for x in s]  
		ss_nested = map(lambda s: map(inc, s), s_nested)  

		print (f"s_nested = {s_nested}")  
		print (f"ss_nested = {ss_nested}")  
		
		
		#Y = (lambda g: lambda f: f(lambda x: g (g) (f) (x))) \  (lambda g: lambda f: f(lambda x: g (g) (f) (x)))  
		Y = ((lambda g: lambda f: f(lambda x: g (g) (f) (x)))(lambda g: lambda f: f(lambda x: g (g) (f) (x))))  	
		
		n = 6
		fibn = Y(lambda f: lambda n: n if n <= 1 else f(n-1) + f(n-2))(n)
		print (f"n = {n} Fibonacci({n}) = {fibn}")  
		
		def square(w):
	return w**2


n = [4,3,2,1]
print(list(map(square, n)))
print(list(map(lambda x : x**2,n)))
print(list(map(lambda x : square(x),n)))
print('..')
		
		
		def get_sub(x):
			
			return('888')
		
		p1 = (lambda x: x[4:8])('2022_01_07.CSV')
		print(p1)
			
		
		p1 = (lambda x: x[0:10] if x[4:8] == '_01_' else('twoooo'))('2022_01_07.CSV')
		print(p1)
		
		def greetings():
			start ='Hallo'
			greet = lambda y: start + str(y)
			return greet 
		result = greetings()
		print(type(result))
		print(result(' RKn'))
		
		def greetings_01():
			start ='Hallo '
			greet = lambda x, y: start + 'Herr' + str(x) if y== 'H' else start + 'Frau'+ x
			return greet
		result = greetings_01()
		print(type(result))
		print(result(' RKn', 'H'))
		print(result(' BKn', 'a'))
		
		
		
		
		p = lambda x: print(x)

		p("Hello")
		p("World")
		
		
		def print_01(a):
			print(a)
		
		f1 = lambda x: print_01(x)
		f1('hgjhjh') 
		
		
		f2 = list(map(lambda x: print_01(x), list_fn))
		
		
		colors = ["Goldenrod", "Purple", "Salmon", "Turquoise", "Cyan"]
		def normalize_case(string):
			return string.casefold()

		normalized_colors = map(normalize_case, colors)
		
		normalized_colors_01 = map(lambda s: s.casefold(), colors)
		normalized_colors_02 = list(sorted(colors, key=lambda s: s.casefold()))
		#print(normalized_colors_02)
		
		#A REGULAR FUNCTION
		def guru( funct, *args ):
			funct( *args )
	
		def printer_one(arg ):
			return print (arg)
	
		def printer_two(*arg ):
			print(arg)
	
		#CALL A REGULAR FUNCTION 
		guru( printer_one, 'printer 1 REGULAR CALL' )
		guru( printer_two, 'printer 2 REGULAR CALL \n' )
	
		#CALL A REGULAR FUNCTION THRU A LAMBDA
		guru(lambda: printer_one('printer 1 LAMBDA CALL'))
		guru(lambda: printer_two('printer 2 LAMBDA CALL', 'hhjhjhjhj'))
		'''
	

