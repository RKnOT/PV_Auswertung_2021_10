import os
import sys

#print(os.cpu_count())
#print(sys.platform)


class Get_CSV_File_Names():
    
    def __init__(self, dir, ext ='.CSV'):
        self.cwd_dir = ''
        self.fileNamesSizeTublesArray = ''
        self.stat=''
        self.fl =[]
        self.fl_fs = []
        self.get_from_dir_file_names(dir, ext)
            
    def get_from_dir_file_names(self, dir,ext):
        try:
            cwd = os.getcwd()
            os.chdir(dir)
            self.dir_files = os.getcwd()
            self.fl  = list(filter(lambda x: x if ext in x else [], os.listdir()))
            self.fileNamesSizeTublesArray  = list(map(lambda x: (x, os.path.getsize(x)), self.fl))
            self.stat = f'{len(self.fl)} files mit der Extension: {ext} gefunden'
        except:
            self.fl.append(-1)
            self.fileNamesSizeTublesArray(-1)
            self.dir_files = os.getcwd() + '/' + dir
            self.stat = 'directory does not exists:\n' + self.dir_files
        finally:
            os.chdir(cwd)
            self.cwd_dir = os.getcwd()



destination ='PVDataLog'
csv_file_names = Get_CSV_File_Names(destination) 
print(len(csv_file_names.fl))
print(len(csv_file_names.fileNamesSizeTublesArray))
print(csv_file_names.stat)
