This project aims at pre-processing times-series raw data to assist researchers/engineers/analysts to analyze their data using spreadsheet softwares by

- re-organizing value-of-change data with inconsistent time intervals to that with constant time intervals
- filling in invalid values in data by interpolation
- align data in multiple worksheets in a spreadsheet file with the same time span
- skip rows with duplicated entries of the same time instants to avoid potential error

This software is useful to preprocess

- building management system (BMS) or Central Control and Monitoring System (CCMS) data with value-of-change data
- environmental data with invalid data
- economic or stock data with gaps in weekends and holidays, and you want space-fillers for them
- etc.

# Introduction

This repository aims at making tools to facilitate data analysis. It provides a 1-page graphical user interface to preprocess BMS data and to facilitate analysis in spreadsheet format.

![](https://github.com/howardcheung/data-preprocessing-helper/raw/master/doc/ui.png "Graphical User Interface")

At the moment, it is able to turn data collected at time-of-change with invalid values

![](https://github.com/howardcheung/auto-data-preprocessor/raw/master/doc/time-of-change.png "Ugly time-of-change data")

to a file which records data at fixed time interval assuming the data
to be a step function

![](https://github.com/howardcheung/auto-data-preprocessor/raw/master/doc/step.png "Preprocessed data assuming step function relationship")

If you want, you can also assume the values to be interpolated values

![](https://github.com/howardcheung/auto-data-preprocessor/raw/master/doc/interpolation.png "Interpolated data")

# Download

The executable (.exe) of the software is only provided for 32-bit and 64-bit Windows. You can download it at [https://github.com/howardcheung/data-preprocessing-helper/releases](https://github.com/howardcheung/data-preprocessing-helper/releases)

For MacOS and Linux users, please try to use [Wine](https://www.winehq.org/). v0.3.8 has been tested with wine-3.0.1 stable in [Linux Mint](https://www.linuxmint.com/) 18.3 and works in it.

# Feedback?

Feel free to post an issue at [https://github.com/howardcheung/data-preprocessing-helper/issues](https://github.com/howardcheung/data-preprocessing-helper/issues) or send me an email at howard (at) gmail.com to let me know the issue!

# Licenses

## License of this software

The source code written in this repository is distributed under the MIT license and is free for personal, academic and commercial use. Details can be found in the file *LICENSE_REPO* in the `LICENSE` directory.

The binaries distributed under releases, due to its inclusion of other modules, are distributed under the GNU GPLv3 license. Details can be found in the file *LICENSE_BINARY* in this directory.

## Notice of third party license agreements

Please notice that the software is developed based on Python 3.5.1 and the binaries contain the following modules:

| Modules | License website |
| ------- | ------- |
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

# Work to be done:
- add intermediate timestamp to the output dataframe
- add tab to choose results depending on time range and weekday ranges

# Diretories and files in the repository
* `changelog`: directory that stores changelog of the software for different versions
* `dat`: directory that stores testing data
* `doc`: directory that stores the user manual
* `exe`: directory that stores instructions on how to compile the binary
* `licenses`: directory that contains licenses of the modules
* `src`: directory that stores the source python script files
* `LICENSE_BINARY`: license file for the software
* `README.md`: file of Markdown script for this readme

# Acknowlegement

The developer(s) would like to acknowledge the inspiration of Prof. Shengwei Wang and Mr. KL William Wu at the Hong Kong Polytechnic University and Dr. Diance Gao at Sun Yat-san University for the creation of this software.
The developer(s) would also like to acknowledge the support of the project *Energy Performance Assessment and Optimization on Buildings in PolyU Campus - Stage 1 and Whole Campus* at the Hong Kong Polytechnic University which needs results in the development of the software.
