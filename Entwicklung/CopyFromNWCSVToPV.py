#!/usr/bin/env python3
import os

#print(os.getcwd())

import UtilsClasses as ut

import concurrent.futures as cf
import time
#from time import sleep 

debug = True

def get_r_l(func):
    wert = func()
    return wert
    
start = time.perf_counter()

#with cf.ThreadPoolExecutor() as executor:
 #   remote = executor.submit(get_r_l, ut.GetNWCSV_File_Names)

#with cf.ThreadPoolExecutor() as executor:
 #       local = executor.submit(get_r_l, ut.Get_CSV_File_Names)

loc = local.result()
        #print(CSV_local.stat)
rem = remote.result()

CSV_local = loc.fileNamesSizeTublesArray
CSV_remote = rem.fileNamesSizeTublesArray

stop = time.perf_counter()

print(f'Time reqired to get NW- and Local-File-Name(s) in {round(stop-start,2)} second(s)')

if debug:
    print('---remote----')
    print('Anzahl der Network Files: ' + str(len(CSV_remote)))
    print(CSV_remote[-1])
    print('-------')
    print('-----local-----')
    print('Anzahl der Local Files: ' + str(len(CSV_local)))
    print(CSV_local[-1])
    print('-------')
 
start = time.perf_counter()

fToCopy =ut.CompareSameFilesRemoteAndLocal(CSV_remote, CSV_local)
if debug: print(fToCopy.fileToUpdate)

copyFile = ut.CopyNWfilesToLocal(fToCopy.fileToUpdate)

stop = time.perf_counter()
print(f'Time reqired to copy file(s) from NW to Local in {round(stop-start,2)} second(s)')
    

