#!/usr/bin/python
"""
    This script file contains methods to define the graphical user interface
    of the tool.

    Author: Howard Cheung
    email: howard.at@gmail.com
"""

# import python internal modules
from calendar import monthrange
from datetime import datetime
from os.path import isfile
from webbrowser import open as webbrowseropen

# import third party modules
import wx

# import user-defined modules


# define global variables
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
            parent, title=title, size=(625, 500)
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

        # define layer size
        begin_depth = 20
        layer_diff = 40
        first_blk = 20
        sec_blk = 200
        third_blk = 475

        # sizer = wx.GridBagSizer(1, 1)  # making a grid in your box

        # title
        # leave space at the top, left and bottom from the text to the
        # other object

        # position: (from top to bottom, from left to right)
        wx.StaticText(panel, label=u''.join([
            u'Time-of-change value data to data',
            u'at constant time intervals'
        ]), pos=(first_blk, begin_depth))

        # Inputs to the data file path
        layer_depth = begin_depth+layer_diff
        text = wx.StaticText(
            panel, label=u'Data file path:',
            pos=(first_blk, layer_depth)
        )

        # require additional object for textbox
        # with default path
        self.dfpath = wx.TextCtrl(
            panel, value=u'../dat/time_of_change.csv',
            pos=(sec_blk, begin_depth+layer_diff), size=(250, 20)
        )
        button = wx.Button(
            panel, label=u'Browse...', pos=(third_blk, layer_depth)
        )
        button.Bind(wx.EVT_BUTTON, self.OnOpen)

        # ask for existence of header as a checkbox
        layer_depth = begin_depth+layer_diff*2
        text = wx.StaticText(
            panel, label=u'Existence of a header row:',
            pos=(first_blk, layer_depth)
        )
        self.header = wx.CheckBox(panel, pos=(sec_blk, layer_depth))
        self.header.SetValue(True)

        # Inputs to the directory to save the plots
        layer_depth += layer_diff
        text = wx.StaticText(
            panel, label=u'Path to save file:', pos=(first_blk, layer_depth)
        )

        # require additional object for textbox
        # with default path
        self.newdfpath = wx.TextCtrl(
            panel, value=u'../testplots/example.csv',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )
        button = wx.Button(
            panel, label=u'Browse...', pos=(third_blk, layer_depth)
        )
        button.Bind(wx.EVT_BUTTON, self.SaveOpen)

        # Inputs to the format time string
        layer_depth += layer_diff
        text = wx.StaticText(panel, label=u''.join([
            u'Format of time string \nin the first column:'
        ]), pos=(first_blk, layer_depth))

        # # require additional object for textbox
        self.timestring = wx.TextCtrl(
            panel, value=u'%m/%d/%y %I:%M:%S %p CST',
            pos=(sec_blk, layer_depth), size=(250, 20)
        )

        # a button for instructions
        button = wx.Button(
            panel,
            label=u'Instructions to enter the format of the time string',
            pos=(sec_blk, layer_depth+20)
        )
        button.Bind(wx.EVT_BUTTON, self.TimeInstruct)

        # add start time input
        layer_depth += (layer_diff+20)
        text = wx.StaticText(panel, label=u''.join([
            u'Start time in the new data file:'
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth))

        # create spin control for the date and time
        self.start_yr = wx.SpinCtrl(
            panel, value='2017', min=1, max=4000,
            pos=(sec_blk, layer_depth), size=(50, 20)
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
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        self.start_day = wx.ComboBox(
            panel, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        self.start_day.SetValue('1')
        text = wx.StaticText(panel, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        self.start_hr = wx.ComboBox(
            panel, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        self.start_hr.SetValue('00')
        text = wx.StaticText(panel, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        self.start_min = wx.ComboBox(
            panel, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        self.start_min.SetValue('00')
        text = wx.StaticText(panel, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))

        # add ending time input
        layer_depth += (layer_diff+20)
        text = wx.StaticText(panel, label=u''.join([
            u'Ending time in the new data file:',
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth))

        # create spin control for the date and time
        self.end_yr = wx.SpinCtrl(
            panel, value='2017', min=1, max=4000,
            pos=(sec_blk, layer_depth), size=(50, 20)
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
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        self.end_day = wx.ComboBox(
            panel, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        self.end_day.SetValue('31')
        text = wx.StaticText(panel, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        self.end_hr = wx.ComboBox(
            panel, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        self.end_hr.SetValue('23')
        text = wx.StaticText(panel, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        self.end_min = wx.ComboBox(
            panel, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        self.end_min.SetValue('59')
        text = wx.StaticText(panel, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))

        # add fixed interval input
        layer_depth += (layer_diff+20)
        text = wx.StaticText(
            panel, label=u'New time interval:',
            pos=(first_blk, layer_depth)
        )
        self.time_int = wx.SpinCtrl(
            panel, value='10', min=1, max=31*24*60,  # max: approx. 1 month
            pos=(sec_blk, layer_depth), size=(50, 20)
        )
        text = wx.StaticText(
            panel, label=u'minutes',
            pos=(sec_blk+50+10, layer_depth+2)
        )

        # buttons at the bottom
        # button_ok = wx.Button(panel, label=u'Analysis')
        # button_ok.Bind(wx.EVT_BUTTON, self.Analyzer)
        # sizer.Add(button_ok, pos=(8, 4))

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
                'csv files (*.csv)|*.csv'
                # 'xls files (*.xls)|*.xls;|',  # to be done
                # 'xlsx files (*.xlsx)|*.xlsx'  # to be done
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

    def Analyzer(self, evt):
        """
            Function to initiate the main analysis.
        """
        # Run the analyzer

        # function to be called upon finishing processing
        wx.CallLater(0, self.ShowMessage)


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
