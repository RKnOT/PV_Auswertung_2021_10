import matplotlib.pyplot as plt
import numpy as np

import json
import os
from datetime import datetime

import UtilsClasses as ut

print(os.getcwd())

'''
import smbprotocol

import uuid

from smbprotocol.connection import Connection, Dialects

connection = Connection(uuid.uuid4(),   '\\pi\d$' , 445)
connection.connect(Dialects.SMB_3_0_2)
'''

from DataModel import GetCSV_File_Names as GetCSV_Names

from DataModel import GetCSV_File_Names as PV_Telegram
from DataModel import TagUtil as TagRecord

print(f'{"-"*40}')


#import smbprotocol
#from smbprotocol.connection import Connection, Dialects

#------------------------------------
class helpers_date_handling():
	def __init__(self, date_time_str = '', debug_flag = False):
		'''
-- helpers_date_handling class --		
Doc Aufruf: 
	print(helpers_date_handling.__init__.__doc__)
date_time_str format -> '2021_12_22 12:44:22' oder '2021_12_22'
Dictionary with the following current date keyes:
	dict_keys(['year_str', 'year_int', 'month_str', 'month_int', 'day_str', 'day_int', 'date_str', 'date_date', 'date_time_str', 'date_time'])
len(datum_dic.keys()) == 1 -> falsches datum -> !! keine datum info !! 

add days:
	t1 = self.datum_dic['current_date_datetime']
	t2 = t1 + datetime.timedelta(days=2)
	print(t2)
		
		'''
		self.datum_dic = {}
		date_time_format = '%Y_%m_%d %H:%M:%S'
		date_format = date_time_format[0:8]
		if date_time_str == '':
			now = datetime.now()
		else:	
			try:
				now = datetime.strptime(date_time_str, date_time_format)
			except: 
				try:
					now = datetime.strptime(date_time_str, date_format)
				except: 
					self.datum_dic['Fehler'] = 'falsches Datum'
					return 
		
		self.datum_dic['year_str'] = now.strftime('%Y')
		self.datum_dic['year_int'] = int(self.datum_dic['year_str'])
		self.datum_dic['month_str'] = now.strftime('%m')
		self.datum_dic['month_int'] = int(self.datum_dic['month_str'])
		self.datum_dic['day_str'] = (now.strftime('%d'))
		self.datum_dic['day_int'] = int(self.datum_dic['day_str'])
		self.datum_dic['date_str'] = self.datum_dic['year_str'] + '_' + self.datum_dic['month_str'] + '_' + self.datum_dic['day_str']
		self.datum_dic['date_date'] = datetime.strptime(self.datum_dic['date_str'], date_format).date()
		self.datum_dic['date_time_str'] = now.strftime(date_time_format)
		self.datum_dic['date_time'] = datetime.strptime(self.datum_dic['date_time_str'], date_time_format)
		if debug_flag: self.debug(self)
			
	
	def date_time_differenz(self, t1, t2):
		diff_dic = {}
		same_date_flag = False
		same_year_flag = False
		same_year_month_flag = False
		if t1.datum_dic['date_date'] == t2.datum_dic['date_date']:
			same_date_flag = True
		if t1.datum_dic['date_date'].year == t2.datum_dic['date_date'].year:
			same_year_flag = True
			if(t1.datum_dic['date_date'].month == t2.datum_dic['date_date'].month):
				same_year_month_flag = True
		diff_dic['time_delta'] = t1.datum_dic['date_time'] - t2.datum_dic['date_time']
		diff_dic['same_date_flag'] = same_date_flag
		diff_dic['same_year_flag'] = same_year_flag
		diff_dic['same_year_month'] = same_year_month_flag
		return diff_dic
	
	def debug(self, hp):
		print(len(self.datum_dic.keys()))
		print()
		print(self.datum_dic.keys())
		print()
		print(self.datum_dic)
		print('end debug_date_handling')
		print()
		
	
		
#--- debug helpers_date_handling ----------
'''
test_date = '2021_12_22'
test_date = '2021_12_22 23:12:00'
hp1 = helpers_date_handling(test_date, debug_flag = True)
hp2 = helpers_date_handling(debug_flag = True)
diff = hp1.date_time_differenz(hp2 , hp1)
print(diff)
'''
#___________________________________________
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
		now = datetime.now()
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
	def years_month_yield(self, years_month_yield):
		years_yield_dic = self.gen_years_yield_empty()
		for k in list(years_month_yield_dic.keys()):
			#print(k)
			#print(years_month_yield_dic[k])
			year_yield = 0.0
			for k1 in years_month_yield_dic[k]:
				#print(k1)
				#print(type(years_month_yield_dic[k][k1]), type(years_month_yield_dic[k][k1]) is dict)
				month_yield_format = "{:8.3f}".format(years_month_yield_dic[k][k1])
				#print("year {}: | month : {} | yield : {}".format(k, k1, month_yield_format))
				year_yield += years_month_yield_dic[k][k1]
			years_yield_dic[k] = year_yield 
		#print('----')	
		#print(years_yield_dic)
		return years_yield_dic
	'---------------'
	def convert_to_bar_plot_lists(self, *args):
		plot_lists = {}
		x = list(args[0].keys())
		X = np.arange(len(x))
		y_n = []
		for item in args:
			y = list(item.values())
			y_n.append(y)
		plot_lists['x_bezeichnung'] = x
		plot_lists['x_werte'] = X
		plot_lists['y_werte_liste'] = y_n
		#print(plot_lists)
		#print('--')
		return plot_lists
	
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
		'''
dict_keys(['last_recorded_date', 'years_month_yield_data', 'years_yield_data_aufgezeichnet', 'years_yield_data_abgerechnet'])
		'''
		
		self.helpers = helpers()
		self.nwd = ut.NetworkData()
		self.nwd.iniData()
		
		self.last_entry_dic = {}
		dir_aggr = 'Aggregation/'
		self.dir_file_dic = {}
		
		#-------------- check year dir exists locally------
		dest = os.path.join(self.nwd.dir_local_CSV, dir_aggr)
		print(dest)
		if os.path.isdir(dest) == False:
			os.mkdir(dest)
		#---------------------------------------------------
		
		self.dir_file_dic['last_recorded_date'] = dest + 'last_recorded_date.json'
		self.dir_file_dic['years_month_yield_data'] = dest + 'years_month_yield_data.json'
		self.dir_file_dic['years_yield_data_aufgezeichnet'] = dest + 'years_yield_data_aufgezeichnet.json'
		self.dir_file_dic['years_yield_data_abgerechnet'] = dest + 'years_yield_data_abgerechnet.json'
		'---------------'
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
		#print(month_1_12)
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
		
		
		def log_datetime(func):
			'''Log the date and time of a function'''
			
			def wrapper():
				print(f'Function: {func.__name__}\nRun on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
				print(f'{"-"*30}')
				func()
			return wrapper


		@log_datetime
		def daily_backup():
			print('Daily backup job has finished.')
			print()
		
		@log_datetime
		def monthly_backup():
			print('Monthly backup job has finished.')
			print()
		
		
		daily_backup()
		monthly_backup()
		
		
		
		print(f'{"_"*30}')
		# Python program to explain os.path.join() method

		# importing os module

		# Path
		path = os.getcwd()

		# Join various path components
		print('1. ' + os.path.join(path, "User/Desktop", "file.txt"))


		# Path
		#path = "User/Documents"

		# Join various path components
		print('2. ' + os.path.join(path, "home", "file22.txt"))

		# In above example '/home'
		# represents an absolute path
		# so all previous components i.e User / Documents
		# are thrown away and joining continues
		# from the absolute path component i.e / home.


		# Path		
		path = "/User"

		# Join various path components
		print('3. ' + os.path.join(path, "Downloads", "file.txt", "/home"))

		# In above example '/User' and '/home'
		# both represents an absolute path
		# but '/home' is the last value
		# so all previous components before '/home'
		# will be discarded and joining will
		# continue from '/home'

		# Path
		path = "/home"

		# Join various path components
		print('4. ' + os.path.join(path, "User/Public/", "Documents", ""))

		# In above example the last
		# path component is empty
		# so a directory separator ('/')
		# will be put at the end
		# along with the concatenated value

		
		print(f'{"_"*30}')
		'''
		def meta_decorator(power):
			def decorator_list(fnc):
				print(type(fnc))
				def inner(list_of_tuples):
					return [(fnc(val[0], val[1])) ** power for val in list_of_tuples]
				return inner
			return decorator_list


		@meta_decorator(3)
		def add_together(a, b):
			return a + b
		

		print(add_together([(1, 3), (3, 17), (5, 5), (6, 7)]))
		'''
		
		
		
		
		
		
		# debug
		#print(helpers_date_handling.__init__.__doc__)
		
		hp = helpers()
		agr = Aggregate_Years_CSV()
		
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
		
		if content == {}:
			print('no date file available')
			#read all years yields
			years_month_yield_dic = agr.aggregate_yield()
			#print(years_yield)
		else: 
			recorted_date_time = list(content.values())[0]
			years_month_yield_dic = hp.readJsonFile(agr.dir_file_dic['years_month_yield_data'])
			#print(list(content.keys())[0])
			#print(hp.datum_dic['date_str'])
			pass
		
		#print(years_month_yield_dic)		
		
		
		#print('current date time: ', current_date_time)
		#print(hp.datum_dic['date_time_str'])
		#print('recorted date time: ', recorted_date_time)
		hp_date_rec = helpers_date_handling(recorted_date_time)
		time_dic = hp_date_rec.date_time_differenz(hp, hp_date_rec)
		print(time_dic.keys())
		print()
		print(time_dic)
		print()
			
	
		
		
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
		print(years_yield_abgerechnet)
		
		# write current date to json
		hp.writeJsonFile(agr.dir_file_dic['last_recorded_date'], current_date_time_record) 
		# write current years month yield to json
		hp.writeJsonFile(agr.dir_file_dic['years_month_yield_data'], years_month_yield_dic) 
		
		# write years yield aufgezeichnet to json
		hp.writeJsonFile(agr.dir_file_dic['years_yield_data_aufgezeichnet'], years_yield_aufgezeichnet) 
		# write years yield abgerechnet to json
		hp.writeJsonFile(agr.dir_file_dic['years_yield_data_abgerechnet'], years_yield_abgerechnet) 
		
		
		'''
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
	

