#!/usr/bin/env python3

import os
import sys

cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')

from CommonClasses.DataModel import TagUtil as TagRecord
from CommonClasses.DMY_Data import  YearView as Y_view
from CommonClasses.DMY_Data import  MonthView as M_view
from CommonClasses.DMY_Data import  DayView as D_view
from CommonClasses.DataModel import GetCSV_File_Names as GetCSV_Names
from CommonClasses.Plot_Graph import  PlotDiagram as Plot
from CommonClasses.Plot_Graph import  Plot_day_view as Pdv
from helper_classes import check_CSV

#-------Eingaben-----------
DaySelected = 24
MonthSelected = 3
YearSelected = 2021
#--
TeleSelected = 2


c= check_CSV(DaySelected, MonthSelected, YearSelected)
v = D_view(c.csv, TeleSelected)

Pdv(v)




#print(c.csv.selected_Day_File)
#print('--------')


#v = D_view(c.csv, 20)
#v = M_view(c.csv)
#v = Y_view(c.csv)
#print(v.A)
