﻿#!/usr/bin/python3
"""
    This script file contains methods to define the graphical user interface
    of the tool.

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/04/11
    License of the source code: MIT license
"""

# import python internal modules
from calendar import monthrange
from datetime import datetime
from os.path import isfile, dirname
from pathlib import Path
from traceback import format_exc
from webbrowser import open as webbrowseropen

# import third party modules
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

class MainGUI(wx.Frame):
    """
        Class to hold the object for the main window of the application
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
        super(MainGUI, self).__init__(
            parent, title=title, size=(700, 700)
        )  # size of the application window

        self.initui()
        self.Centre()
        self.Show()

    def initui(self):
        """
            Initialize the position of objects in the UI
        """

        # define the panel
        panel = wx.Panel(self)

        # create menubar for About information
        menubar = wx.MenuBar()
        helpm = wx.Menu()
        abti = wx.MenuItem(helpm, wx.ID_ABOUT, '&About', 'Program Information')
        self.Bind(wx.EVT_MENU, self.AboutDialog, abti)
        helpm.Append(abti)
        menubar.Append(helpm, '&Help')
        self.SetMenuBar(menubar)

        # define layer size
        begin_depth = 20
        layer_diff = 40
        first_blk = 20
        sec_blk = 250
        third_blk = 525

        # title
        # position: (from top to bottom, from left to right)
        wx.StaticText(panel, label=u''.join([
            u'Time-of-change value data to data',
            u'at constant time intervals'
        ]), pos=(first_blk, begin_depth))

        # Inputs to the data file path
        layer_depth = begin_depth+layer_diff
        text = wx.StaticText(
            panel, label=u'Data file path:',
            pos=(first_blk, layer_depth+2)
        )
        # require additional object for textbox
        # with default path
        self.dfpath = wx.TextCtrl(
            panel, value=u'../dat/time_of_change.csv',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        button = wx.Button(
            panel, label=u'Browse...', pos=(third_blk, layer_depth)
        )
        button.Bind(wx.EVT_BUTTON, self.OnOpen)
        layer_depth += layer_diff

        # ask for existence of header as a checkbox
        text = wx.StaticText(
            panel, label=u'Existence of a header row:',
            pos=(first_blk, layer_depth+2)
        )
        self.header = wx.CheckBox(panel, pos=(sec_blk, layer_depth))
        self.header.SetValue(True)
        # for the positioning of the header numeric function
        wx.StaticText(
            panel, label=u''.join([
                'Number of rows to be skipped\nabove the header row:'
            ]), pos=(third_blk-150, layer_depth), size=(150, 30)
        )
        self.header_no = wx.SpinCtrl(
            panel, value='0', min=0, max=100000,  # max: approx. 1 month
            pos=(third_blk+20, layer_depth),
            size=(50, 20)
        )
        # add the dynamic information of the checkbox
        self.header.Bind(wx.EVT_CHECKBOX, self.HeaderInput)
        layer_depth += layer_diff

        # Inputs to the directory to save the plots
        text = wx.StaticText(
            panel, label=u'Path to save file:', pos=(first_blk, layer_depth+2)
        )
        # require additional object for textbox
        # with default path
        self.newdfpath = wx.TextCtrl(
            panel, value=u'./example.csv',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        button = wx.Button(
            panel, label=u'Browse...', pos=(third_blk, layer_depth)
        )
        button.Bind(wx.EVT_BUTTON, self.SaveOpen)
        layer_depth += layer_diff

        # Separator of output file
        # can be any string, but provide the choices
        wx.StaticText(
            panel, label=u''.join([
                u'Separator of the output file',
                u'\n(valid for csv file only):'
            ]), pos=(first_blk, layer_depth+2)
        )
        # do not use unicode here
        self.output_sep = wx.ComboBox(
            panel, value=',', choices=[';', ','],
            pos=(sec_blk, layer_depth), size=(50, 20)
        )
        layer_depth += layer_diff

        # Inputs to the format time string
        text = wx.StaticText(panel, label=u''.join([
            u'Format of time string \nin the output file:'
        ]), pos=(first_blk, layer_depth+2))
        # # require additional object for textbox
        self.outputtimestring = wx.TextCtrl(
            panel, value=u'%Y/%m/%d %H:%M:%S',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        # a button for instructions
        button = wx.Button(
            panel,
            label=u'Instructions to enter the format of the time string',
            pos=(sec_blk, layer_depth+20)
        )
        button.Bind(wx.EVT_BUTTON, self.TimeInstruct)
        layer_depth += (layer_diff+20)

        # Inputs to the format time string
        text = wx.StaticText(panel, label=u''.join([
            u'Format of time string \nin the first column\n of the input file:'
        ]), pos=(first_blk, layer_depth+2))
        # require additional object for textbox
        self.timestring = wx.TextCtrl(
            panel, value=u'%m/%d/%y %I:%M:%S %p CST',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        # a button for instructions
        text = wx.StaticText(panel, label=u''.join([
            u'Same instructions as the format in output file'
        ]), pos=(sec_blk, layer_depth+20))
        layer_depth += (layer_diff+20)

        # add start time input
        text = wx.StaticText(panel, label=u''.join([
            u'Start time in the new data file:'
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth+2))

        # create spin control for the date and time
        self.start_yr = wx.SpinCtrl(
            panel, value='2017', min=1, max=4000,
            pos=(sec_blk, layer_depth), size=(55, 20)
        )
        text = wx.StaticText(panel, label=u''.join([
            u'Year'
        ]), pos=(sec_blk, layer_depth+20))
        # reset the last day of the month if needed
        self.start_yr.Bind(wx.EVT_COMBOBOX, self.ChangeStartDayLimit)

        self.start_mon = wx.ComboBox(
            panel, pos=(sec_blk+70, layer_depth),
            choices=[str(ind) for ind in range(1, 13)], size=(50, 20)
        )
        self.start_mon.SetValue('1')
        # reset the last day of the month if needed
        self.start_mon.Bind(wx.EVT_COMBOBOX, self.ChangeStartDayLimit)
        self.start_mon.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        self.start_day = wx.ComboBox(
            panel, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        self.start_day.SetValue('1')
        self.start_day.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        self.start_hr = wx.ComboBox(
            panel, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        self.start_hr.SetValue('00')
        self.start_hr.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        self.start_min = wx.ComboBox(
            panel, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        self.start_min.SetValue('00')
        self.start_min.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))
        layer_depth += (layer_diff+20)

        # add ending time input
        text = wx.StaticText(panel, label=u''.join([
            u'Ending time in the new data file:',
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth+2))

        # create spin control for the date and time
        self.end_yr = wx.SpinCtrl(
            panel, value='2017', min=1, max=4000,
            pos=(sec_blk, layer_depth), size=(55, 20)
        )
        text = wx.StaticText(panel, label=u''.join([
            u'Year'
        ]), pos=(sec_blk, layer_depth+20))
        # reset the last day of the month if needed
        self.end_yr.Bind(wx.EVT_COMBOBOX, self.ChangeEndDayLimit)

        self.end_mon = wx.ComboBox(
            panel, pos=(sec_blk+70, layer_depth),
            choices=[str(ind) for ind in range(1, 13)], size=(50, 20)
        )
        self.end_mon.SetValue('12')
        # reset the last day of the month if needed
        self.end_mon.Bind(wx.EVT_COMBOBOX, self.ChangeEndDayLimit)
        self.end_mon.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        self.end_day = wx.ComboBox(
            panel, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        self.end_day.SetValue('31')
        self.end_day.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        self.end_hr = wx.ComboBox(
            panel, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        self.end_hr.SetValue('23')
        self.end_hr.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        self.end_min = wx.ComboBox(
            panel, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        self.end_min.SetValue('59')
        self.end_min.SetEditable(False)
        text = wx.StaticText(panel, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))
        self.no_endtime = wx.CheckBox(panel, pos=(sec_blk+70*5, layer_depth+2))
        self.no_endtime.SetValue(True)
        wx.StaticText(
            panel, label=u'Autogen\nending time',
            pos=(sec_blk+70*5, layer_depth+20)
        )
        layer_depth += (layer_diff+20)

        # add fixed interval input
        text = wx.StaticText(
            panel, label=u'New time interval:',
            pos=(first_blk, layer_depth+2)
        )
        self.time_int = wx.SpinCtrl(
            panel, value='10', min=1, max=31*24*60,  # max: approx. 1 month
            pos=(sec_blk, layer_depth), size=(50, 20)
        )
        text = wx.StaticText(
            panel, label=u'minutes',
            pos=(sec_blk+50+10, layer_depth+2)
        )
        layer_depth += layer_diff

        # Relationship between time series data points
        wx.StaticText(
            panel, label=u'Assumption between data points:',
            pos=(first_blk, layer_depth+2)
        )
        self.func_choice = wx.ComboBox(
            panel, value=u'Step Function',
            choices=[
                u'Step Function',
                u'Continuous variable (inter- and extrapolation)'
            ], pos=(sec_blk, layer_depth), size=(225, 20)
        )
        self.func_choice.SetSelection(0)
        self.func_choice.SetEditable(False)
        layer_depth += layer_diff

        # Assumptions on extrapolation
        wx.StaticText(
            panel, label=u''.join([
                u'Assumptions for data points\n',
                u'earlier than the existing data:'
            ]), pos=(first_blk, layer_depth+2)
        )
        self.early_pts = wx.ComboBox(
            panel, value=u'Use the minimum value in the trend',
            choices=[
                u'Use the minimum value in the trend',
                u'Use the first value in the trend'
            ], pos=(sec_blk, layer_depth), size=(225, 20)
        )
        self.early_pts.SetSelection(0)
        self.early_pts.SetEditable(False)
        layer_depth += layer_diff

        # buttons at the bottom
        button_ok = wx.Button(
            panel, label=u'Preprocess', pos=(third_blk+50, layer_depth)
        )
        button_ok.Bind(wx.EVT_BUTTON, self.Analyzer)
        layer_depth += layer_diff

    def ShowMessage(self):
        """
            Function to show message about the completion of the analysis
        """
        wx.MessageBox(
            u'Processing Completed', u'Status', wx.OK | wx.ICON_INFORMATION
        )

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

        if not isfile(filepath):
            wx.LogError('Cannot open file "%s".' % openFileDialog.GetPath())
            return False

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

    def HeaderInput(self, evt):
        """
            Function to allow input of file header informaiton if the
            existence of a header is confirmed
        """
        if evt.IsChecked():
            self.header_no.Enable(True)
        else:
            self.header_no.Enable(False)

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

    def AboutDialog(self, evt):
        """
            Function to show the dialog box for About Information
        """

        info = adv.AboutDialogInfo()
        info.SetName('Data Preprocessing Helper')
        info.SetVersion('0.2.1')
        info.SetDescription(DESCRIPTION)
        info.SetCopyright('(C) Copyright 2017 Howard Cheung')
        info.SetWebSite(
            'https://github.com/howardcheung/data-preprocessing-helper/'
        )
        info.SetLicence(LICENSE)
        info.AddDeveloper('Howard Cheung [howard.at (at) gmail.com]')
        adv.AboutBox(info)

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
            datadf = read_data(
                self.dfpath.GetValue(),
                header=(self.header_no.GetValue() if header_exist else None),
                time_format=self.timestring.GetValue()
            )
            convert_df(
               datadf, start_time,
               (None if self.no_endtime.GetValue() else end_time),
               interval=int(self.time_int.GetValue())*60,
               step=(True if self.func_choice.GetSelection()==0 else False),
               ini_val=self.early_pts.GetSelection()+1,
               output_file=self.newdfpath.GetValue(),
               sep=self.output_sep.GetValue(),
               output_timestring=self.outputtimestring.GetValue()
            )
        except BaseException:
            box = wx.MessageDialog(
                self, format_exc(), u'Error', wx.OK | wx.ICON_INFORMATION
            )
            box.Fit()
            box.ShowModal()
            return

        # function to be called upon finishing processing
        wx.CallLater(0, self.ShowMessage)
        evt.Skip()


# define functions
def gui_main():
    """
        Main function to intiate the GUI
    """
    app = wx.App()
    MainGUI(None, title=u'Data Preprocessing Helper')
    app.MainLoop()


# run the method for the GUI
if __name__ == '__main__':
    gui_main()
