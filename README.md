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
- organize the license files of the modules 

# Diretories
* `dat`: directory that stores testing data
* `doc`: directory that stores the user manual
* `src`: directory that stores the source python script files
* `licenses`: directory that contains licenses of the modules

# Licenses

## License of this software

The source code written in this repository is distributed under the MIT license and is free for personal, academic and commercial use. Details can be found in the file *LICENSE_REPO* in this directory.

The binaries distributed under releases, due to its inclusion of other modules, are distributed under the GNU GPLv3 license. Details can be found in the file *LICENSE_BINARY* in this directory.

## Notice of third party license agreements

Please notice that the software is developed based on Python 3.5.1 and the binaries contain the following modules:

| Modules | License website |
| :-----: | :-----: |
| appdirs (1.4.3) | [Link](https://github.com/ActiveState/appdirs/blob/master/LICENSE.txt) |
| future (0.16.0) | [Link](http://python-future.org/credits.html) |
| numpy (1.12.1) | [Link](http://www.numpy.org/license.html) |
| packaging (16.8) | [Link](https://github.com/pypa/packaging/blob/master/LICENSE.BSD) |
| pandas (0.19.2) | [Link](http://pandas.pydata.org/pandas-docs/stable/overview.html#license) |
| pip (9.0.1) | [Link](https://github.com/pypa/pip/blob/master/LICENSE.txt) |
| PyInstaller (3.2.1) | [Link](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt) |
| pyparsing (2.2.0) | [Link](https://sourceforge.net/projects/pyparsing/files/pyparsing/pyparsing-2.2.0/) (in source tarball) |
| pypiwin32 (219) | [Link](https://github.com/pywin32/pypiwin32/blob/master/LICENSE) |
| python-dateutil (2.6.0) | [Link](https://github.com/dateutil/dateutil/blob/master/LICENSE) |
| pytz (2017.2) | [Link](https://pythonhosted.org/pytz/index.html#license) |
| setuptools (34.4.1) | [Link](https://github.com/pypa/setuptools/blob/master/LICENSE) |
| six (1.10.0) | [Link](https://pypi.python.org/pypi/six/) (in source tarball) |
| wheel (0.29.0) | [Link](https://bitbucket.org/pypa/wheel/src/54ddbcc9cec25e1f4d111a142b8bfaa163130a61/LICENSE.txt?at=default) |
| wxPython-Phoenix (3.0.3.dev2891+36b8076) | [Link](https://github.com/wxWidgets/Phoenix/blob/fb52c7a66ec9c156a781822e9e4680b3eae7d27f/wx/lib/pubsub/LICENSE_BSD_Simple.txt) |
| xlrd (1.0.0) | [Link](https://github.com/python-excel/xlrd/blob/fcfdb721abe650c0b25d8a874dc7314e9eb8dc59/docs/licenses.rst) |
| XlsxWriter (0.9.6) | [Link](https://github.com/jmcnamara/XlsxWriter/blob/master/LICENSE.txt) |
| xlwt (1.2.0) | [Link](https://github.com/python-excel/xlwt/blob/917a8ad8db35d6e8abb306a2fda2ace648a6ab89/docs/licenses.rst) |

The licenses of these modules are included in the directory LICENSE.
