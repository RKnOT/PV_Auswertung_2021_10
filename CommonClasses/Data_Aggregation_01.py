
import json
import os


import UtilsClasses as ut


from DataModel import GetCSV_File_Names as GetCSV_Names

from DataModel import GetCSV_File_Names as PV_Telegram
from DataModel import TagUtil as TagRecord
'''
Aggregations Stufen

Years:	2012 -> Month 1-12 -> Day 01-31

										 							
list {'2012': {'10': ['17', '18', .. , '31'], '11' : ['01', '02', .., '30'], '12': ['01', '02', .. ,'30', '31']}, '2013': {...}}


'''






class Aggregate_Year_CSV():
	def __init__(self):
		self.nwd = ut.NetworkData()
		self.nwd.iniData()
		self.dir_aggr = 'Aggregation'
		#-------------- check year dir exists locally------
		self.dest = self.nwd.dir_local_CSV + '/' + self.dir_aggr + '/'
	
		if os.path.isdir(self.dest) == False:
			os.mkdir(dest)
		#---------------------------------------------------
        
		I_get_csv_file_names = ut.Get_CSV_File_Names_from_Dir()
		self.dic_y_m_d = I_get_csv_file_names.years_month_days_dic
		#print()
		#self.check_dirs_exists()
		self.aggregate_yield()
		
	def writeJsonFile(self, dest, file_content):
		with open(dest, 'w') as outfile:
			json.dump(file_content, outfile)
			pass
	def readJsonFile(self):  
		if os.path.exists(jsonDat):
			with open(jsonDat) as json_file:
				self.data = json.load(json_file)
		else: self.data =[]
		pass

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
				
		print(year_file_names['Years'])
		print(year_month_names)		
		
		
		for item in year_file_names['Years']:
			dest = self.dest + item
			#print(dest)
			# Writing to sample.json
			#self.writeJsonFile(dest, dictionary)
			#break		
		pass
	
	
	def aggregate_yield(self):  
		
		dm = TagRecord()
		list_day_yield_pro_month = []
		years_month_yields = {}
		key_years = list(self.dic_y_m_d.keys())
		#print(key_years)
		for key_year in key_years:
		
			month = list(self.dic_y_m_d[key_year].keys())
			year_month_yield =[]
				
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
				year_month_yield.append(monthYield)
				#years_month_yields[key_year] = month_yield
				#print(key_year, key_month, monthYield) 
			
			print(year_month_yield)
				#break #Debug
		
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
		
		out = lambda *x: print(' & '.join(map(str, x)))
		a = out(1, 2, 3, 'hallo', 'gp1')
		
		
		
		Year_list = ['2012', '2013', '2014', '2015', '2020', '2021', '2022']
		tuple1 = ()
		tuple2 = ()
		#tuple3 = ()
		for i in range(0, len(Year_list)):
			tuple1 = (*tuple1, Year_list[i])
		print(tuple1)
		for i in range(0, len(Year_list)):
			tuple2 = (*tuple2, Year_list[i])
		print(tuple2)
		
		tuple3 =   lambda x: x, Year_list""
		
		print(tuple3)
		#Aggregate_Year_CSV()
		
		
		'''
		
		list_fn = ['2022_01_01.CSV', '2022_01_02.CSV', '2022_01_03.CSV', '2022_01_04.CSV', '2022_01_05.CSV', '2022_01_06.CSV', '2022_01_07.CSV', '2022_01_08.CSV', '2022_01_09.CSV', '2022_01_10.CSV', '2022_01_11.CSV', '2022_01_12.CSV', '2022_01_13.CSV', '2022_01_14.CSV', '2022_01_15.CSV', '2022_01_16.CSV', '2022_01_17.CSV', '2022_01_18.CSV', '2022_01_19.CSV', '2022_01_20.CSV', '2022_01_21.CSV', '2022_01_22.CSV', '2022_01_23.CSV', '2022_01_24.CSV', '2022_01_25.CSV', '2022_01_26.CSV', '2022_01_27.CSV', '2022_01_28.CSV', '2022_01_29.CSV', '2022_01_30.CSV', '2022_01_31.CSV', '2022_02_01.CSV', '2022_02_02.CSV', '2022_02_03.CSV', '2022_02_04.CSV', '2022_02_05.CSV', '2022_02_06.CSV', '2022_02_07.CSV', '2022_02_08.CSV', '2022_02_09.CSV', '2022_02_10.CSV', '2022_02_11.CSV', '2022_02_12.CSV', '2022_02_13.CSV', '2022_02_14.CSV', '2022_02_15.CSV', '2022_02_16.CSV', '2022_02_17.CSV', '2022_02_18.CSV', '2022_02_19.CSV', '2022_02_20.CSV', '2022_02_21.CSV', '2022_02_22.CSV', '2022_02_23.CSV', '2022_02_24.CSV', '2022_02_25.CSV', '2022_02_26.CSV', '2022_02_27.CSV', '2022_02_28.CSV', '2022_03_01.CSV', '2022_03_02.CSV', '2022_03_03.CSV', '2022_03_04.CSV', '2022_03_05.CSV', '2022_03_06.CSV', '2022_03_07.CSV', '2022_03_08.CSV', '2022_03_09.CSV', '2022_03_10.CSV', '2022_03_11.CSV', '2022_03_12.CSV', '2022_03_13.CSV', '2022_03_14.CSV', '2022_03_15.CSV', '2022_03_16.CSV']
		
		m_list = ['_01_', '_02_', '_03_', '_04_','_05_', '_06_', '_07_', '_08_', '_09_', '_10_', '_11_', '_12_'] 	
			
		
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
	
