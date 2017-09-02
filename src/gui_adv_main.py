#!/usr/bin/python3
"""
    This script file contains methods to define the graphical user interface
    of the tool with basic setting for beginners and advanced setting for
    flexibility

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/08/29
    License of the source code: MIT license
"""

# import python internal modules
from calendar import monthrange
from datetime import datetime
from math import isnan
from ntpath import split
from os.path import isfile, dirname
from pathlib import Path
from traceback import format_exc
from webbrowser import open as webbrowseropen

# import third party modules
from pandas import ExcelFile
import wx
from wx import adv

# import user-defined modules
from data_read import read_data
from format_data import convert_df


# define global variables
DESCRIPTION = \
"""Data Preprocessing Helper is a software made to
help people to preprocess their data that contain ugly
features such as time-of-change values, blank values, etc
to nicely presented data with no blank values
"""
LICENSE = \
"""GNU GENERAL PUBLIC LICENSE Version 3
Data Preprocessing Helper
Copyright (C) 2017 Howard Cheung

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For licenses of modules involved in the development of the software,
please visit <https://github.com/howardcheung/data-preprocessing-helper/>
"""

# classes for tabs
# Template from https://wiki.wxpython.org/Simple%20wx.Notebook%20Example
class BasicTab(wx.Panel):
    """
        The first tab
    """
    def __init__(self, parent, frame):
        """
            This is the initilization function for the tab.

            Inputs:
            ==========
            parent: wx.Notebook
                parent object

            frame: ex.Frame
                the parent frame object
        """
        super(BasicTab, self).__init__(parent)
        
        # define layer size
        begin_depth = 20
        layer_diff = 40
        first_blk = 20
        sec_blk = 250
        third_blk = 525

        # title
        # position: (from top to bottom, from left to right)
        wx.StaticText(self, label=u''.join([
            u'Basic settings for beginners'
        ]), pos=(first_blk, begin_depth))

        # Inputs to the data file path
        layer_depth = begin_depth+layer_diff
        text = wx.StaticText(
            self, label=u'Data file path:',
            pos=(first_blk, layer_depth+2)
        )
        # require additional object for textbox
        # with default path
        frame.dfpath = wx.TextCtrl(
            self, value=u'../dat/time_of_change.csv',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        # load worksheet name choices for files with xls/ xlsx extension
        # for self.sheetname ComboBox
        frame.dfpath.Bind(wx.EVT_TEXT, frame.ChangeForXlsFile)
        button = wx.Button(
            self, label=u'Browse...', pos=(third_blk, layer_depth)
        )
        button.Bind(wx.EVT_BUTTON, frame.OnOpen)
        layer_depth += layer_diff

        # ask for existence of header as a checkbox
        text = wx.StaticText(
            self, label=u'Existence of a header row:',
            pos=(first_blk, layer_depth+2)
        )
        frame.header = wx.CheckBox(self, pos=(sec_blk, layer_depth))
        frame.header.SetValue(True)
        # for the positioning of the header numeric function
        wx.StaticText(
            self, label=u''.join([
                'Number of rows to be skipped\nabove the header row:'
            ]), pos=(third_blk-150, layer_depth), size=(150, 30)
        )
        frame.header_no = wx.SpinCtrl(
            self, value='0', min=0, max=100000,  # max: approx. 1 month
            pos=(third_blk+20, layer_depth),
            size=(50, 20)
        )
        # add the dynamic information of the checkbox
        frame.header.Bind(wx.EVT_CHECKBOX, frame.HeaderInput)
        layer_depth += layer_diff

        # Inputs to the directory to save the plots
        text = wx.StaticText(
            self, label=u'Path to save file:', pos=(first_blk, layer_depth+2)
        )
        # require additional object for textbox
        # with default path
        frame.newdfpath = wx.TextCtrl(
            self, value=u'./example.csv',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        frame.newdfpath.Bind(wx.EVT_TEXT, frame.ChangeForXlsFileOutput)
        button = wx.Button(
            self, label=u'Browse...', pos=(third_blk, layer_depth)
        )
        button.Bind(wx.EVT_BUTTON, frame.SaveOpen)
        layer_depth += layer_diff
        # add start time input
        text = wx.StaticText(self, label=u''.join([
            u'Start time in the new data file:'
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth+2))

        # create spin control for the date and time
        frame.start_yr = wx.SpinCtrl(
            self, value='2017', min=1, max=4000,
            pos=(sec_blk, layer_depth), size=(55, 20)
        )
        text = wx.StaticText(self, label=u''.join([
            u'Year'
        ]), pos=(sec_blk, layer_depth+20))
        # reset the last day of the month if needed
        frame.start_yr.Bind(wx.EVT_COMBOBOX, frame.ChangeStartDayLimit)

        frame.start_mon = wx.ComboBox(
            self, pos=(sec_blk+70, layer_depth),
            choices=[str(ind) for ind in range(1, 13)], size=(50, 20)
        )
        frame.start_mon.SetValue('1')
        # reset the last day of the month if needed
        frame.start_mon.Bind(wx.EVT_COMBOBOX, frame.ChangeStartDayLimit)
        frame.start_mon.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        frame.start_day = wx.ComboBox(
            self, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        frame.start_day.SetValue('1')
        frame.start_day.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        frame.start_hr = wx.ComboBox(
            self, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        frame.start_hr.SetValue('00')
        frame.start_hr.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        frame.start_min = wx.ComboBox(
            self, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        frame.start_min.SetValue('00')
        frame.start_min.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))
        frame.use_starttime = wx.CheckBox(
            self, pos=(sec_blk+70*5, layer_depth+2)
        )
        frame.use_starttime.SetValue(True)
        wx.StaticText(
            self, label=u'Use file\nstarting time',
            pos=(sec_blk+70*5, layer_depth+20),
            size=(75, 30)
        )  # set size to (75,30) to push the right border for space in panel
        layer_depth += (layer_diff+20)

        # add ending time input
        text = wx.StaticText(self, label=u''.join([
            u'Ending time in the new data file:',
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth+2))

        # create spin control for the date and time
        frame.end_yr = wx.SpinCtrl(
            self, value='2017', min=1, max=4000,
            pos=(sec_blk, layer_depth), size=(55, 20)
        )
        text = wx.StaticText(self, label=u''.join([
            u'Year'
        ]), pos=(sec_blk, layer_depth+20))
        # reset the last day of the month if needed
        frame.end_yr.Bind(wx.EVT_COMBOBOX, frame.ChangeEndDayLimit)

        frame.end_mon = wx.ComboBox(
            self, pos=(sec_blk+70, layer_depth),
            choices=[str(ind) for ind in range(1, 13)], size=(50, 20)
        )
        frame.end_mon.SetValue('12')
        # reset the last day of the month if needed
        frame.end_mon.Bind(wx.EVT_COMBOBOX, frame.ChangeEndDayLimit)
        frame.end_mon.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        frame.end_day = wx.ComboBox(
            self, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        frame.end_day.SetValue('31')
        frame.end_day.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        frame.end_hr = wx.ComboBox(
            self, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        frame.end_hr.SetValue('23')
        frame.end_hr.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        frame.end_min = wx.ComboBox(
            self, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        frame.end_min.SetValue('59')
        frame.end_min.SetEditable(False)
        text = wx.StaticText(self, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))
        frame.no_endtime = wx.CheckBox(self, pos=(sec_blk+70*5, layer_depth+2))
        frame.no_endtime.SetValue(True)
        wx.StaticText(
            self, label=u'Autogen\nending time',
            pos=(sec_blk+70*5, layer_depth+20)
        )
        layer_depth += (layer_diff+20)

        # add fixed interval input
        text = wx.StaticText(
            self, label=u'New time interval in the output file:',
            pos=(first_blk, layer_depth+2)
        )
        frame.time_int = wx.SpinCtrl(
            self, value='10', min=1, max=31*24*60,  # max: approx. 1 month
            pos=(sec_blk, layer_depth), size=(50, 20)
        )
        text = wx.StaticText(
            self, label=u'minutes',
            pos=(sec_blk+50+10, layer_depth+2)
        )
        layer_depth += layer_diff


class AdvancedTab(wx.Panel):
    """
        The second tab
    """
    def __init__(self, parent, frame):
        """
            This is the initilization function for the tab.

            Inputs:
            ==========
            parent: wx.Frame
                parent object

            frame: ex.Frame
                the parent frame object
        """
        super(AdvancedTab, self).__init__(parent)
        
        # define layer size
        begin_depth = 20
        layer_diff = 40
        first_blk = 20
        sec_blk = 250
        third_blk = 525

        # title
        # position: (from top to bottom, from left to right)
        wx.StaticText(self, label=u''.join([
            u'Advanced settings for more flexible but complex settings'
        ]), pos=(first_blk, begin_depth))

        # option to select sheet, if any, and choose if all sheets
        # should be loaded
        layer_depth = begin_depth+layer_diff
        wx.StaticText(self, label=u''.join([
            u'For xls/xlsx input files only:'
        ]), pos=(first_blk, layer_depth))
        layer_depth = layer_depth+layer_diff*0.75
        wx.StaticText(self, label=u''.join([
            u'Choose a worksheet to load\n',
            u'for xls/xlsx input file:'
        ]), pos=(first_blk, layer_depth-5))
        frame.sheetname = wx.ComboBox(
            self, pos=(sec_blk, layer_depth), size=(100, 30)
        )
        frame.sheetname.Enable(False)
        wx.StaticText(self, label=u''.join([
            u'Load all worksheets with the\n',
            u'same config for xls/xlsx input file:'
        ]), pos=(third_blk-150, layer_depth-5))
        frame.loadallsheets = wx.CheckBox(
            self, pos=(third_blk+55, layer_depth)
        )
        frame.loadallsheets.SetValue(False)
        if 'xls' not in get_ext(frame.dfpath.GetValue()):
            frame.loadallsheets.Enable(False)
        # check if anything needs to be changed after
        # checking/unchecking the box
        frame.loadallsheets.Bind(wx.EVT_CHECKBOX, frame.LoadAllSheets)
        layer_depth += layer_diff

        # Separator of output file
        # can be any string, but provide the choices
        layer_depth += layer_diff/2.0
        wx.StaticText(self, label=u''.join([
            u'For csv output files only:'
        ]), pos=(first_blk, layer_depth))
        layer_depth = layer_depth+layer_diff/2.0
        wx.StaticText(
            self, label=u''.join([
                u'Separator of the output file:'
            ]), pos=(first_blk, layer_depth)
        )
        # do not use unicode here
        frame.output_sep = wx.ComboBox(
            self, value=',', choices=[';', ','],
            pos=(sec_blk, layer_depth), size=(50, 20)
        )
        layer_depth += layer_diff

        # Inputs to the format time string
        layer_depth += layer_diff/2.0
        wx.StaticText(self, label=u''.join([
            u'Output/Input time string in the first column of the data file:'
        ]), pos=(first_blk, layer_depth))
        layer_depth = layer_depth+layer_diff/2.0
        text = wx.StaticText(self, label=u'\n'.join([
            u'Format of time string', u'in the output file',
            u'(invalid for xls/xlsx file output):'
        ]), pos=(first_blk, layer_depth+2))
        # # require additional object for textbox
        frame.outputtimestring = wx.TextCtrl(
            self, value=u'%Y/%m/%d %H:%M:%S',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        frame.outputtimestring.Enable(
            get_ext(frame.dfpath.GetValue()) == 'csv'
        )
        # a button for instructions
        button = wx.Button(
            self,
            label=u'Instructions to enter the format of the time string',
            pos=(sec_blk, layer_depth+layer_diff/2.0)
        )
        button.Bind(wx.EVT_BUTTON, frame.TimeInstruct)
        layer_depth += (layer_diff+layer_diff/2.0)

        # other output format
        wx.StaticText(self, label=u'\n'.join([
            u'or output the time as values of ',
        ]), pos=(first_blk, layer_depth+2))
        frame.numtimeoutput = wx.ComboBox(self, value='None', choices=[
            'None', 'seconds', 'minutes', 'hours', 'days'
        ], pos=(sec_blk, layer_depth), size=(70, 20))
        frame.numtimeoutput.SetEditable(False)
        frame.numtimeoutput.Bind(wx.EVT_COMBOBOX, frame.ChangeOptionForNum)
        wx.StaticText(self, label=u'\n'.join([
            u'from the user-defined start time',
        ]), pos=(sec_blk+80, layer_depth+2))
        layer_depth += (layer_diff)

        # Inputs to the format time string
        text = wx.StaticText(self, label=u'\n'.join([
            u'Format of time string in the first',
            u'column of the input file:'
        ]), pos=(first_blk, layer_depth+2))
        # require additional object for textbox
        frame.timestring = wx.TextCtrl(
            self, value=u'%m/%d/%y %I:%M:%S %p CST',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        # Computer to auto-detect the format instead
        frame.autotimeinputformat = wx.CheckBox(
            self, pos=(sec_blk+70*4, layer_depth+2)
        )
        frame.autotimeinputformat.SetValue(True)
        wx.StaticText(
            self, label=u'Auto-detecting format\nof input time string',
            pos=(sec_blk+70*4, layer_depth+20)
        )
        frame.autotimeinputformat.Bind(
            wx.EVT_CHECKBOX, frame.GreyOutInputTimeString
        )
        frame.timestring.Enable(False)  # disable the option
        # a button for instructions
        text = wx.StaticText(self, label=u''.join([
            u'Same instructions as the format in output file'
        ]), pos=(sec_blk, layer_depth+20))
        layer_depth += (layer_diff+20)

        # Relationship between time series data points
        layer_depth += layer_diff/2.0
        wx.StaticText(self, label=u''.join([
            u'Assumptions on data structure in the input file:'
        ]), pos=(first_blk, layer_depth))
        layer_depth = layer_depth+layer_diff/2.0
        wx.StaticText(
            self, label=u'Assumption between data points:',
            pos=(first_blk, layer_depth+2)
        )
        frame.func_choice = wx.ComboBox(
            self, value=u'Step Function',
            choices=[
                u'Step Function',
                u'Continuous variable (inter- and extrapolation)'
            ], pos=(sec_blk, layer_depth), size=(225, 20)
        )
        frame.func_choice.SetSelection(0)
        frame.func_choice.SetEditable(False)
        layer_depth += layer_diff

        # Assumptions on extrapolation
        wx.StaticText(
            self, label=u''.join([
                u'Assumptions for data points\n',
                u'earlier than the existing data:'
            ]), pos=(first_blk, layer_depth+2)
        )
        frame.early_pts = wx.ComboBox(
            self, value=u'Use the minimum value in the trend',
            choices=[
                u'Use the minimum value in the trend',
                u'Use the first value in the trend',
                u'Use blanks'
            ], pos=(sec_blk, layer_depth), size=(225, 20)
        )
        frame.early_pts.SetSelection(2)
        frame.early_pts.SetEditable(False)
        layer_depth += layer_diff


class MainFrame(wx.Frame):
    """
        Frame holding the tabs
    """
    def __init__(self, parent, title):
        """
            This is the initilization function for the GUI.

            Inputs:
            ==========
            parent: wx.Frame
                parent object

            title: str
                title of the window
        """
        super(MainFrame, self).__init__(
            parent, title=title, size=(720, 770),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )  # size of the application window

        self.Centre()

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)

        # create menubar for About information
        menubar = wx.MenuBar()
        helpm = wx.Menu()
        abti = wx.MenuItem(helpm, wx.ID_ABOUT, '&About', 'Program Information')
        self.Bind(wx.EVT_MENU, self.AboutDialog, abti)
        helpm.Append(abti)
        menubar.Append(helpm, '&Help')
        self.SetMenuBar(menubar)

        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        # pass the frame into it to make the frame event functions available
        page1 = BasicTab(nb, frame=self)
        page2 = AdvancedTab(nb, frame=self)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Basic")
        nb.AddPage(page2, "Advanced")

        # create button
        button_ok = wx.Button(p, label=u'Preprocess', size=(100, 30))
        button_ok.Bind(wx.EVT_BUTTON, self.Analyzer)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 15, 0, border=10)  # 25 for space under the advanced tab
        sizer.Add(button_ok, 1, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=5)
        sizer.SetSizeHints(self)
        self.SetSizerAndFit(sizer)

    # define all event functions here
    def AboutDialog(self, evt):
        """
            Function to show the dialog box for About Information
        """

        info = adv.AboutDialogInfo()
        info.SetName('Data Preprocessing Helper')
        info.SetVersion('0.3.5')
        info.SetDescription(DESCRIPTION)
        info.SetCopyright('(C) Copyright 2017 Howard Cheung')
        info.SetWebSite(
            'https://github.com/howardcheung/data-preprocessing-helper/'
        )
        info.SetLicence(LICENSE)
        info.AddDeveloper('Howard Cheung [howard.at (at) gmail.com]')
        adv.AboutBox(info)

    def OnClose(self, evt):
        """
            Function to close the main window
        """
        self.Close(True)
        evt.Skip()

    def OnOpen(self, evt):
        """
            Function to open a file
            Reference:
            https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        """
        # proceed asking to the user the new directory to open
        openFileDialog = wx.FileDialog(
            self, 'Open file', '', '',
            ''.join([
                'csv files (*.csv)|*.csv;|',
                'xls files (*.xls)|*.xls;|',
                'xlsx files (*.xlsx)|*.xlsx'
            ]), wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return False  # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filepath = openFileDialog.GetPath()
        self.dfpath.SetValue(filepath)

        # check if file exists
        if not isfile(filepath):
            wx.LogError('Cannot open file "%s".' % openFileDialog.GetPath())
            return False

        # load worksheet name choices for files with xls/ xlsx extension
        # for self.sheetname ComboBox
        self.ChangeForXlsFile(evt)

    def ChangeForXlsFile(self, evt):
        """
            Change options if the input file is an excel file
        """
        # load worksheet name choices for files with xls/ xlsx extension
        # for self.sheetname ComboBox
        filepath = self.dfpath.GetValue()
        ext = get_ext(filepath)
        if ext == 'xls' or ext == 'xlsx':
            self.loadallsheets.Enable(True)
            if not self.loadallsheets.GetValue():
                self.sheetname.Enable(True)
            try:  # the file may not exist
                with ExcelFile(filepath) as xlsx:
                    sheetnames = xlsx.sheet_names
                    self.sheetname.SetItems(sheetnames)
                    self.sheetname.SetValue(sheetnames[0])
            except FileNotFoundError:
                pass
        else:
            self.loadallsheets.Enable(False)
            self.loadallsheets.SetValue(False)  # reset loading all worksheets
            self.sheetname.Enable(False)

    def HeaderInput(self, evt):
        """
            Function to allow input of file header informaiton if the
            existence of a header is confirmed
        """
        if evt.IsChecked():
            self.header_no.Enable(True)
        else:
            self.header_no.Enable(False)

    def LoadAllSheets(self, evt):
        """
            To disable the selection of the sheets based on the selection
            of the option of loadallsheet
        """
        if self.loadallsheets.GetValue():
            self.sheetname.Enable(False)
        else:
            self.sheetname.Enable(True)

    def SaveOpen(self, evt):
        """
            Function to open a file
            Reference:
            https://wxpython.org/Phoenix/docs/html/wx.DirDialog.html
        """
        # proceed asking to the user the new file to open

        openFileDialog = wx.FileDialog(
            self, 'Open file', '', '',
            ''.join([
                'csv files (*.csv)|*.csv;|',
                'xls files (*.xls)|*.xls;|',
                'xlsx files (*.xlsx)|*.xlsx'
            ]), wx.FD_SAVE
        )

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return False  # the user changed idea...

        # proceed saving the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filepath = openFileDialog.GetPath()
        self.newdfpath.SetValue(filepath)

        # change GUI as needed
        self.ChangeForXlsFileOutput(evt)

    def ChangeForXlsFileOutput(self, evt):
        """
            Change options if the output file is an excel file
        """
        filepath = self.newdfpath.GetValue()
        ext = get_ext(filepath)
        if ext == 'xls' or ext == 'xlsx':
            # no longer need output time string setting
            self.outputtimestring.Enable(False)
        else:
            if self.numtimeoutput.GetValue() == 'None':
                self.outputtimestring.Enable(True)

    def TimeInstruct(self, evt):
        """
            Function to open instructions for time string
        """
        webbrowseropen(
            u''.join([
                u'https://docs.python.org/3.5/library/datetime.html',
                u'#strftime-and-strptime-behavior'
            ])
        )

    def ChangeOptionForNum(self, evt):
        """
            Change options for number values
        """
        if self.numtimeoutput.GetValue() != 'None':
            self.outputtimestring.Enable(False)
        else:
            self.ChangeForXlsFileOutput(evt)

    def GreyOutInputTimeString(self, evt):
        """
            Grey out input time string when the auto-detection option is
            selected
        """
        if self.autotimeinputformat.GetValue():
            self.timestring.Enable(False)
        else:
            self.timestring.Enable(True)

    def ChangeStartDayLimit(self, evt):
        """
            Function to change the limit of the starting day selection
            based on the selection of the year and the month
        """
        # find the number of days based on the current configuration
        lastday = monthrange(
            int(self.start_yr.GetValue()), int(self.start_mon.GetValue())
        )[1]
        # check the current selection. Set it to the last day of the month
        # if the current selection exceed the new last day
        if int(self.start_day.GetValue()) > lastday:
            self.start_day.SetValue(str(lastday))
        # add days to fit monthrange
        while self.start_day.GetCount() < lastday:
            self.start_day.Append(str(self.start_day.GetCount()+1))
        # remove days to fit monthrange
        while self.start_day.GetCount() > lastday:
            self.start_day.Delete(self.start_day.GetCount()-1)
        evt.Skip()

    def ChangeEndDayLimit(self, evt):
        """
            Function to change the limit of the starting day selection
            based on the selection of the year and the month
        """
        # find the number of days based on the current configuration
        lastday = monthrange(
            int(self.end_yr.GetValue()), int(self.end_mon.GetValue())
        )[1]
        # check the current selection. Set it to the last day of the month
        # if the current selection exceed the new last day
        if int(self.end_day.GetValue()) > lastday:
            self.end_day.SetValue(str(lastday))
        # add days to fit monthrange
        while self.end_day.GetCount() < lastday:
            self.end_day.Append(str(self.end_day.GetCount()+1))
        # remove days to fit monthrange
        while self.end_day.GetCount() > lastday:
            self.end_day.Delete(self.end_day.GetCount()-1)
        evt.Skip()

    def Analyzer(self, evt):
        """
            Function to initiate the main analysis.
        """
        # check all required inputs
        # check the existence of the folder
        if not isfile(self.dfpath.GetValue()):
            wx.MessageBox(
                u'Cannot open the data file!', u'Error',
                wx.OK | wx.ICON_INFORMATION
            )
            return
        # check the existence of the saving path
        if not Path(dirname(self.newdfpath.GetValue())).exists():
            box = wx.MessageDialog(
                self, u'Saving directory does not exist!', u'Error',
                wx.OK | wx.ICON_INFORMATION
            )
            box.Fit()
            box.ShowModal()
            return
        # check file type
        ext = get_ext(self.newdfpath.GetValue())
        if not (ext == 'csv' or ext == 'xls' or ext == 'xlsx'):
            box = wx.MessageDialog(
                self, u'Output file type not supported!', u'Error',
                wx.OK | wx.ICON_INFORMATION
            )
            box.Fit()
            box.ShowModal()
            return
        # check the time
        start_time = datetime(
            int(self.start_yr.GetValue()), int(self.start_mon.GetValue()),
            int(self.start_day.GetValue()), int(self.start_hr.GetValue()),
            int(self.start_min.GetValue())
        )
        end_time = datetime(
            int(self.end_yr.GetValue()), int(self.end_mon.GetValue()),
            int(self.end_day.GetValue()), int(self.end_hr.GetValue()),
            int(self.end_min.GetValue())
        )
        if not self.no_endtime.GetValue() and start_time > end_time:
            wx.MessageBox(
                u'Starting time later than ending time!', u'Error',
                wx.OK | wx.ICON_INFORMATION
            )
            return

        # Run the analyzer
        # output any error to a message box if needed
        try:
            header_exist = self.header.GetValue()
            datadfs = read_data(
                self.dfpath.GetValue(),
                header=(self.header_no.GetValue() if header_exist else None),
                time_format=self.timestring.GetValue(),
                sheetnames=(
                    [] if self.loadallsheets.GetValue() else (
                        None
                        if get_ext(self.dfpath.GetValue()) == 'csv'
                        else [self.sheetname.GetValue()]
                    )
                ), dateautodetect=self.autotimeinputformat.GetValue()
            )
            # return error if load all sheet option is selected for csv file
            # output
            if get_ext(self.newdfpath.GetValue()) == 'csv' and \
                    self.loadallsheets.GetValue() and \
                    len(datadfs) > 1:
                wx.MessageBox(
                    u'\n'.join([
                        u'Cannot output multiple worksheets to a csv file!',
                        u'Please output it as a xls or xlsx file!'
                    ]), u'Error',
                    wx.OK | wx.ICON_INFORMATION
                )
                return
            # show warning for columns that contain no valid data
            for sheet_name in datadfs:
                datadf = datadfs[sheet_name]
                for col in datadf.columns:
                    if all([
                        isinstance(x, str) or isnan(x)
                        for x in datadf.loc[:, col]
                    ]):
                        dlg = MessageDlg(''.join([
                                'Column ', col, ' in ', sheet_name, 
                                ' does not contain any valid values.',
                                ' Closing in 2s......'
                            ]), u'Warning')        
                        wx.CallLater(2000, dlg.Destroy)
                        dlg.ShowModal()
            convert_df(
               datadfs, (None if self.use_starttime.GetValue() else start_time),
               (None if self.no_endtime.GetValue() else end_time),
               interval=int(self.time_int.GetValue())*60,
               step=(True if self.func_choice.GetSelection() == 0 else False),
               ini_val=self.early_pts.GetSelection()+1,
               output_file=self.newdfpath.GetValue(),
               sep=self.output_sep.GetValue(),
               output_timestring=self.outputtimestring.GetValue(),
               outputtimevalue=self.numtimeoutput.GetValue()
            )
        except BaseException:
            # box = wx.MessageDialog(
                # self, format_exc(), u'Error', wx.OK | wx.ICON_INFORMATION
            # )
            chgdep = ErrorReportingDialog(None)
            chgdep.ShowModal()
            chgdep.Destroy()
            return

        # function to be called upon finishing processing
        wx.CallLater(0, self.ShowMessage)
        evt.Skip()

    def ShowMessage(self):
        """
            Function to show message about the completion of the analysis
        """
        wx.MessageBox(
            u'Processing Completed', u'Status', wx.OK | wx.ICON_INFORMATION
        )


class MessageDlg(wx.Dialog):
    """
        Function for auto-closing message diaglog
        from https://stackoverflow.com/questions/6012380/wxmessagebox-with-an-auto-close-timer-in-wxpython
    """
    def __init__(self, message, title):
        """
            Initailizing a new dialog box that can be closed automatically
        """
        wx.Dialog.__init__(self, None, -1, title, size=(400, 120))
        self.CenterOnScreen(wx.BOTH)

        ok = wx.Button(self, wx.ID_OK, "OK")
        ok.SetDefault()
        text = wx.StaticText(self, -1, message)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(text, 1, wx.ALIGN_CENTER | wx.TOP, 10)
        vbox.Add(ok, 1, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        self.SetSizer(vbox)


class ErrorReportingDialog(wx.Dialog):
    """
        Error Diaglog box
        from http://zetcode.com/wxpython/dialogs/
    """

    def __init__(self, *args, **kw):
        """
            Initializing the dialog box
        """
        super(ErrorReportingDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((500, 400))
        self.SetTitle(u'Error')

    def InitUI(self):
        """
            Interface of the error dialog box
        """

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label=u''.join([
            u'Process failed. Please report your situation with the following error messages:'
        ]))
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        sbs.Add(wx.TextCtrl(
            pnl, value=format_exc(), size=(475, 400),
            style=wx.TE_READONLY | wx.TE_MULTILINE
        ))

        pnl.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, e):
        """
            Close the error dialog box
        """

        self.Destroy()


# define functions
def gui_main():
    """
        Main function to intiate the GUI
    """
    app = wx.App()
    MainFrame(None, title=u'Data Preprocessing Helper').Show()
    app.MainLoop()


def get_ext(filepath: str) -> str:
    """
        Return the extension of a file given a file path

        Inputs:
        ==========
        filepath: str
            string character for a filepath
    """

    return split(filepath)[1].split('.')[-1]


if __name__ == "__main__":
    gui_main()
