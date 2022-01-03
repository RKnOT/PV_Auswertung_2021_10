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
import threading

#------ thread task
def doit(stop_event, arg, c, max_count = 25):
    
    print ("%s thread gestarted" % arg)
    while not stop_event.wait(1):
        
        print(str(c), '\r', end='')
        c +=1
        if c > max_count:
           print("\n%s max Zählerstand erreicht" % arg)
           break
          
    
    print("\n%s thread beendet" % arg)

#----------

#test
#-----------Debug Einstellungen-------
debug = False
debug_write_file = False
# files kopieren
file_copy_flag = True # True > files werden kopiert // False > files werden nicht kopiert
#-------------------------------------


def get_r_l(func):
    wert = func()
    return wert
   
print('remote und lokale Files lesen')
print('')

start = time.perf_counter()
if platform.system() != 'Windows':
    
    pill2kill = threading.Event()
    
    count = 0
    
    
    t = threading.Thread(target=doit, args=(pill2kill, "Read local and remote files", count))
    
    # start t-event
    t.start()
    with cf.ThreadPoolExecutor() as executor:
        try:
            rem = executor.submit(get_r_l, ut.GetNWCSV_File_Names).result()
            #print('\nNetzerk nicht verfügbar\n')
        
        except IndexError: 
            print("Error: please provide a name and a repeat count to the script.")
            sys.exit(1)
            
        with cf.ThreadPoolExecutor() as executor:
                loc = executor.submit(get_r_l, ut.Get_CSV_File_Names).result()
        
        CSV_local = loc.fileNamesSizeTublesArray
        CSV_remote = rem.fileNamesSizeTublesArray
    
    # stop event
    pill2kill.set()
    #t.join()
    
else: # Window environment
    nw = ut.Get_Write_Windows_Network_Files()
    CSV_remote = nw.fileNamesSizeTublesArray

    loc = ut.Get_CSV_File_Names()
    CSV_local = loc.fileNamesSizeTublesArray
    if debug_write_file:
        with open('CSV_remote.txt', 'w') as f:
            for item in CSV_remote:
                f.write(item[0]+ ' | ' + str(item[1]))
                f.write('\n')
        with open('CSV_local.txt', 'w') as f:
            for item in CSV_local:
                f.write(item[0]+ ' | ' + str(item[1]))
                f.write('\n')

stop = time.perf_counter()

'''
if rem.NW_flag:
    print('remote und lokale Files gelesen')
    print('-----------')
'''

print(f'Time reqired to get NW- and Local-File-Name(s) in {round(stop-start,2)} second(s)')


if debug:
        print('---remote----')
        print('Anzahl der Network Files: ' + str(len(CSV_remote)-1))
        if CSV_remote !=[]: 
            print(CSV_remote[-1])
            print('-------')
            print('-----local-----')
            print('Anzahl der Local Files: ' + str(len(CSV_local)-1))
        if CSV_local !=[]: 
            print(CSV_local[-1])
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
        #print(copyFile.copied_files)
        if len(copyFile.copied_files) > 0:
            for f_names in copyFile.copied_files:
                print(f_names)
            print('--------------')
        
        
        
        print(f'Time reqired to copy file(s) from NW to Local in {round(stop-start,2)} second(s)')
else: 
            print('keine files kopiert')



