# Data Preprocessing Helper
This project wraps up the pre-processing routine in other projects to help others to preprocess the data without coding work

# Introduction

This repository aims at making tools to facilitate data analysis. At the moment,
it is able to turn data collected at time-of-change with invalid values

![](https://github.com/howardcheung/auto-data-preprocessor/raw/Documentation/doc/time-of-change.png "Ugly time-of-change data")

to a file which records data at fixed time interval assuming the data
to be a step function

![](https://github.com/howardcheung/auto-data-preprocessor/raw/Documentation/doc/step.png "Preprocessed data assuming step function relationship")

If you want, you can also assume the values to be interpolated values

![](https://github.com/howardcheung/auto-data-preprocessor/raw/Documentation/doc/interpolation.png "Interpolated data")


# Work to be done:
- add intermediate timestamp to the output dataframe
- use upx to reduce the size of the executable
- write the user manual

# Diretories
* `dat`: directory that stores testing data
* `doc`: directory that stores the user manual
* `src`: directory that stores the source python script files

# Licenses

Please check the document LICENSE for license issue of this software. The software is developed under Python 3.5.1 and the following python modules:

* appdirs (1.4.3)
* future (0.16.0)
* numpy (1.12.1)
* packaging (16.8)
* pandas (0.19.2)
* pip (9.0.1)
* PyInstaller (3.2.1)
* pyparsing (2.2.0)
* pypiwin32 (219)
* python-dateutil (2.6.0)
* pytz (2017.2)
* setuptools (34.4.1)
* six (1.10.0)
* virtualenv (15.1.0)
* wheel (0.29.0)
* wxPython-Phoenix (3.0.3.dev2891+36b8076)
* xlrd (1.0.0)
* XlsxWriter (0.9.6)
* xlwt (1.2.0)

Please check their websites for their licenses as well.
