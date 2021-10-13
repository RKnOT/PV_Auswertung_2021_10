#!/usr/bin/env python3

import os
import sys
from datetime import datetime

cwd = os.getcwd()
sys.path.insert(1, cwd + '/CommonClasses')

from CommonClasses.DataModel import TagUtil as TagRecord
from CommonClasses.DMY_Data import  YearView as Y_view
from CommonClasses.DMY_Data import  MonthView as M_view
from CommonClasses.DMY_Data import  DayView as D_view
from CommonClasses.DataModel import GetCSV_File_Names as GetCSV_Names
from CommonClasses.Plot_Graph import  PlotDiagram as Plot
from CommonClasses.Plot_Graph import  Plot_day_view as Pdv

"""
Using an UIKit view.
"""
import pyto_ui as ui
from UIKit import UIDatePicker
from Foundation import NSObject
from rubicon.objc import objc_method, SEL
from datetime import datetime

# We subclass ui.UIKitView to implement a date picker

#-------Eingaben-----------
DaySelected = 24
MonthSelected = 3
YearSelected = 2021
#--
TeleSelected = 2
#--------------------
class check_CSV():
    def __init__(self, print_flag = False):
        path_csvFiles = "PVDataLog"
        self.datestr = str(YearSelected) +'_'+ str(MonthSelected).zfill(2)+ '_'+ str(DaySelected).zfill(2)    
        self.csv = GetCSV_Names(path_csvFiles, self.datestr)
        if print_flag: print(self.csv.status)
#-------------------


c= check_CSV()
v = D_view(c.csv, TeleSelected)

class DatePicker(ui.UIKitView):
    
    did_change = None
    #print(dir(ui.UIKitView))
    # Here we return an UIDatePicker object
    def make_view(self):
        picker = UIDatePicker.alloc().init()
        
         # We create an Objective-C instance that will respond to the date picker value changed event
        delegate = PickerDelegate.alloc().init()
        delegate.picker = self
        delegate.objc_picker = picker
        
        # 4096 is the value for UIControlEventValueChanged
        picker.addTarget(delegate, action=SEL("didChange"), forControlEvents=4096)
        return picker
    
# An Objective-C class for addTarget(_:action:forControlEvents:)
class PickerDelegate(NSObject):

    picker = None

    @objc_method
    def didChange(self):
        if self.picker.did_change is not None:
            date = self.objc_picker.date
            #date = datetime.fromtimestamp(date.timeIntervalSince1970())
            self.picker.did_change(date)
            

# Then we can use our date picker as any other view

view = ui.View()
view.background_color = ui.COLOR_SYSTEM_BACKGROUND

def did_change(date):
    view.title = str(date)
    #dateStr = date.strftime("%Y_%m_%d")
    print(date)
    
    #Pdv(v)
    print(c.csv.status)
date_picker = DatePicker()
date_picker.did_change = did_change

#print(dir(date_picker))

date_picker.flex = [
    ui.FLEXIBLE_BOTTOM_MARGIN,
    ui.FLEXIBLE_TOP_MARGIN,
    ui.FLEXIBLE_LEFT_MARGIN,
    ui.FLEXIBLE_RIGHT_MARGIN
]
date_picker.center = view.center
view.add_subview(date_picker)

ui.show_view(view, ui.PRESENTATION_MODE_SHEET)