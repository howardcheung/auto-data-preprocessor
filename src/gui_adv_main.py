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
    def __init__(self, parent):
        """
            This is the initilization function for the tab.

            Inputs:
            ==========
            parent: wx.Frame
                parent object
        """
        super(BasicTab, self).__init__(parent)
        t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))


class AdvancedTab(wx.Panel):
    """
        The second tab
    """
    def __init__(self, parent):
        """
            This is the initilization function for the tab.

            Inputs:
            ==========
            parent: wx.Frame
                parent object
        """
        super(AdvancedTab, self).__init__(parent)
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40,40))


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

        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = BasicTab(nb)
        page2 = AdvancedTab(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Basic")
        nb.AddPage(page2, "Advanced")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)  # add the notebook to the frame directly


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


# define functions
def gui_main():
    """
        Main function to intiate the GUI
    """
    app = wx.App()
    MainFrame(None, title=u'Data Preprocessing Helper').Show()
    app.MainLoop()


if __name__ == "__main__":
    gui_main()
