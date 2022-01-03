#!/usr/bin/env python3
import os
import sys
import platform
cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')
import CommonClasses.UtilsClasses as ut
import concurrent.futures as cf
import time
import datetime


#-----------Debug Einstellungen-------
debug = False
# files kopieren
file_copy_flag = True # True > files werden kopiert // False > files werden nicht kopiert
#-------------------------------------


def get_r_l(func):
    wert = func()
    return wert
   
print('remote und lokale Files lesen')
print('-----------')
start = time.perf_counter()
if platform.system() != 'Windows':

    nw = ut.GetNWCSV_File_Names
    with cf.ThreadPoolExecutor() as executor:
        remote = executor.submit(get_r_l, nw)
    with cf.ThreadPoolExecutor() as executor:
        local = executor.submit(get_r_l, ut.Get_CSV_File_Names)
        loc = local.result()
        rem = remote.result()
        CSV_local = loc.fileNamesSizeTublesArray
        CSV_remote = rem.fileNamesSizeTublesArray
else: # Window environment
    nw = ut.Get_Write_Windows_Network_Files()
    CSV_remote = nw.fileNamesSizeTublesArray

    loc = ut.Get_CSV_File_Names()
    CSV_local = loc.fileNamesSizeTublesArray

stop = time.perf_counter()

print('remote und lokale Files gelesen')
print('-----------')


print(f'Time reqired to get NW- and Local-File-Name(s) in {round(stop-start,2)} second(s)')


if debug:
    print('---remote----')
    print('Anzahl der Network Files: ' + str(len(CSV_remote)))
    if CSV_remote !=[]: print(CSV_remote[-1])
    print('-------')
    print('-----local-----')
    print('Anzahl der Local Files: ' + str(len(CSV_local)))
    if CSV_local !=[]: print(CSV_local[-1])
    print('-------')

if file_copy_flag:
    print('Files von remote nach local kopieren')
    print('------------')
    
    start = time.perf_counter()

    fToCopy =ut.CompareSameFilesRemoteAndLocal(CSV_remote, CSV_local)
    if debug: print(fToCopy.fileToUpdate)
    
    copyFile = ut.CopyNWfilesToLocal(fToCopy.fileToUpdate, file_copy_flag)

    stop = time.perf_counter()
    print(str(copyFile.count) + ' Files kopiert')
    print('--------------')
    print(f'Time reqired to copy file(s) from NW to Local in {round(stop-start,2)} second(s)')
else: print('keine files kopiert')
