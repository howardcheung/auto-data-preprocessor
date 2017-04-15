# Using virtual environment to make a smaller executable by the following code

```
virtualenv -p <Path to python exe> <name of project>
cd ./<name of project>/Scripts/
activate.bat
pip install <wheel for wxPython Pheonix>
pip install pandas
pip install xlwt
pip install xlsxwriter
pip install xlrd
pip install pyinstaller
pip install pypiwin32
```

and use the installed pyinstaller in the virtual environment python directory to do

```
<directory of the local pyinstaller>\pyinstalled.exe ..\src\gui_main.py
```

to create the executable.

# Using standalone embedded Python 3.5 on Windows

To build th executable with embedded Python, you first need to install the
modules mentioned above with the embedded Python. Once you have done so, you
need to

* Extract materials in python35.zip to a directory called python35.zip in the same embedded python directory (reference to be added later)
* Extract pyconfig.h to the Include directory from the PC directory in the source tarball (tested on Windows only)
* Replace all .pyc files in python35.zip directory by the corresponding .py files (or your base_library directory is not going to get the right files)

Use the pyinstaller.exe in the Script directory of your embedded python to compile ..\src\gui_main.py for the executable
