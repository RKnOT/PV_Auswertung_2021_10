'''
import os
import sys

from datetime import datetime

cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')

#from CommonClasses.DataModel import GetCSV_File_Names as GetCSV_Names


 save current dir
 directory auf read write file setzen 
 auf current dir zurücksetzten
 
 
 get all files with exe "xxx"
 
 read content of a file
 
 write content string, list
 
 read string, manipulate content, write content back 
 
'''
#-------------
import sys
import os

cwd = os.getcwd()
print(os.path.basename(os.getcwd()))

os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
print(os.path.basename(os.getcwd()))


os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
print(os.path.basename(os.getcwd()))



print(os.getcwd())
os.chdir(cwd)

print(os.getcwd())
'''



#---------------------
class sub_dir_Names():
    def __init__(self):
        self.path_csvFiles = "PVDataLog"
        #---
        self.CSV_Path_O_Log ='/PV_Anlage_Log_Daten/LOG_PV_2016_01_01_Original'
        self.CSV_Path_N_Log ='/PV_Anlage_Log_Daten/'
        #---
        self.CSV_Path_O_Mega ='/LOG_MEGA_128'
        self.CSV_Path_N_Mega ='/LOG_MEGA_128/2014'

#---------------------
class get_imports(sub_dir_Names):
    
    def __init__(self):
        import os
        import sys
        from glob import glob
        super().__init__()
        self.cwd = os.getcwd()
        self.root = os.path.dirname(self.cwd)
        
        daf = os.listdir(self.root)
        print(daf)
        print('-----')
        for i in daf:
            
                if os.path.isdir(self.root +'/'+i):
                    print(i)
                    #print(self.root+ '/' +i)
        #print(glob('*'))
        #print('----')
        #print(os.path.splitdrive(self.cwd))
        self.print_list(sys.path)
        #print('---')
        sys.path.insert(1, self.cwd + '/CommonClasses')
        self.print_list(sys.path)

    def print_list(self, list): 
        print('--- print list start----')
        for i in list:
            print(i)
            print('----')
        print('---print list end')

#---------------------
        
        
print(os.pardir)



gi = get_imports()
#print(gi.root)
#print(gi.CSV_Path_O_Log)
