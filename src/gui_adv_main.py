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
            u'Basic setting for beginners'
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
            u'Advanced setting for more flexible but complex settings'
        ]), pos=(first_blk, begin_depth))

        # option to select sheet, if any, and choose if all sheets
        # should be loaded
        layer_depth = begin_depth+layer_diff
        wx.StaticText(self, label=u''.join([
            u'For xls/xlsx files only:'
        ]), pos=(first_blk, layer_depth))
        layer_depth = layer_depth+layer_diff
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
            parent, title=title, size=(720, 770)
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

        nb = wx.Notebook(parent=p)

        # create the page windows as children of the notebook
        page1 = BasicTab(nb, frame=self)
        page2 = AdvancedTab(nb, frame=self)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Basic")
        nb.AddPage(page2, "Advanced")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)  # add the notebook to the frame directly

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
