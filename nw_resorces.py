
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

network = ut.GetNW()
