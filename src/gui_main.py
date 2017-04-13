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
            parent, title=title, size=(625, 550)
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
        layer_depth += layer_diff

        # Inputs to the directory to save the plots
        text = wx.StaticText(
            panel, label=u'Path to save file:', pos=(first_blk, layer_depth+2)
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
        layer_depth += layer_diff

        # Separator of output file
        # can be any string, but provide the choices
        wx.StaticText(
            panel, label=u''.join([
                u'Separator of the output file:'
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
            u'Format of time string \nin the first column:'
        ]), pos=(first_blk, layer_depth+2))

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
        layer_depth += (layer_diff+20)

        # add start time input
        text = wx.StaticText(panel, label=u''.join([
            u'Start time in the new data file:'
            u'\n(inaccurate for too much extension)'
        ]), pos=(first_blk, layer_depth+2))

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
        self.start_mon.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        self.start_day = wx.ComboBox(
            panel, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        self.start_day.SetValue('1')
        self.start_day.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        self.start_hr = wx.ComboBox(
            panel, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        self.start_hr.SetValue('00')
        self.start_hr.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        self.start_min = wx.ComboBox(
            panel, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        self.start_min.SetValue('00')
        self.start_min.Bind(wx.EVT_TEXT, self.SelfChecker)
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
        self.end_mon.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(sec_blk+70, layer_depth+20))

        self.end_day = wx.ComboBox(
            panel, pos=(sec_blk+70*2, layer_depth),
            choices=[str(ind) for ind in range(1, 32)], size=(50, 20)
        )
        self.end_day.SetValue('31')
        self.end_day.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Day'
        ]), pos=(sec_blk+70*2, layer_depth+20))

        self.end_hr = wx.ComboBox(
            panel, pos=(sec_blk+70*3, layer_depth),
            choices=['%02i' % ind for ind in range(24)], size=(50, 20)
        )
        self.end_hr.SetValue('23')
        self.end_hr.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Hour'
        ]), pos=(sec_blk+70*3, layer_depth+20))

        self.end_min = wx.ComboBox(
            panel, pos=(sec_blk+70*4, layer_depth),
            choices=['%02i' % ind for ind in range(60)], size=(50, 20)
        )
        self.end_min.SetValue('59')
        self.end_min.Bind(wx.EVT_TEXT, self.SelfChecker)
        text = wx.StaticText(panel, label=u''.join([
            u'Minutes'
        ]), pos=(sec_blk+70*4, layer_depth+20))

        # add fixed interval input
        layer_depth += (layer_diff+20)
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
                u'Step Function', u'Continuous variable (coming soon)'
            ], pos=(sec_blk, layer_depth), size=(200, 20)
        )
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
            ], pos=(sec_blk, layer_depth), size=(200, 20)
        )
        layer_depth += layer_diff

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
        evt.Skip()

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
        evt.Skip()

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
        evt.Skip()

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

    def SelfChecker(self, evt):
        """
            Check values of ComboBoxes. If they do not match the
            permissible values. Reset them to the first value available
        """
        if not self.start_mon.GetValue().isdigit() or \
                int(self.start_mon.GetValue()) < 1 or \
                int(self.start_mon.GetValue()) > 12:
            self.start_mon.SetValue('1')
        if not self.start_day.GetValue().isdigit() or \
                int(self.start_day.GetValue()) < 1 or \
                int(self.start_day.GetValue()) > 31:
            self.start_day.SetValue('1')
        if not self.start_hr.GetValue().isdigit() or \
                int(self.start_hr.GetValue()) < 1 or \
                int(self.start_hr.GetValue()) > 23:
            self.start_hr.SetValue('00')
        if not self.start_min.GetValue().isdigit() or \
                int(self.start_min.GetValue()) < 1 or \
                int(self.start_min.GetValue()) > 59:
            self.start_min.SetValue('00')
        if not self.end_mon.GetValue().isdigit() or \
                int(self.end_mon.GetValue()) < 1 or \
                int(self.end_mon.GetValue()) > 12:
            self.end_mon.SetValue('1')
        if not self.end_day.GetValue().isdigit() or \
                int(self.end_day.GetValue()) < 1 or \
                int(self.end_day.GetValue()) > 31:
            self.end_day.SetValue('1')
        if not self.end_hr.GetValue().isdigit() or \
                int(self.end_hr.GetValue()) < 1 or \
                int(self.end_hr.GetValue()) > 23:
            self.end_hr.SetValue('00')
        if not self.end_min.GetValue().isdigit() or \
                int(self.end_min.GetValue()) < 1 or \
                int(self.end_min.GetValue()) > 59:
            self.end_min.SetValue('00')
        evt.Skip()

    def Analyzer(self, evt):
        """
            Function to initiate the main analysis.
        """
        # check all required inputs
        if not isfile(self.dfpath.GetValue()):
            wx.MessageBox(
                u'Cannot open the data file!', u'Status',
                wx.OK | wx.ICON_INFORMATION
            )
            return

        # Run the analyzer

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
