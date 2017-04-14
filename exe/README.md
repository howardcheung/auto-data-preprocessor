# Need to use virtual environment to make a smaller executable by the following code

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