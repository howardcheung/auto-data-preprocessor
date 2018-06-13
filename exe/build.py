#!/usr/bin/python3
"""
    This file runs operating system functions to compile and build
    the executables in the directories and copy them to the corresponding
    directories.

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/07/23
    License of the source code: MIT license
"""

from distutils.dir_util import copy_tree
import os
import subprocess
from shutil import copyfile, rmtree
import zipfile

# define variables
VERSION = '0.3.8'

BITS = ['win32', 'amd64']
for BIT in BITS:
    # create executables using embedded python
    print('Building the', BIT, 'application')
    subprocess.check_call([
        ''.join(['../python-3.5.3-embed-', BIT, '/python.exe']),
        '-m',
        'PyInstaller',  # calling the pyinstaller
        '--onefile',  # one file executable
        '-w',  # no console io
        '-y',  # overwrite existing files
        '--clean',  # clean to avoid corrupting the next build
        '../src/gui_adv_main.py'  # the GUI python file
    ])

    # copy the created file to the releases directory
    REQ_DIRS = [
        ''.join(['../releases/v', VERSION, '/']),
        ''.join([
            '../releases/v', VERSION,
            '/DataPreprocessingHelper-v', VERSION, '-', BIT
        ])
    ]
    for REQ_DIR in REQ_DIRS:
        if not os.path.exists(REQ_DIR):
            os.makedirs(REQ_DIR)

    # copy the files
    copyfile('./dist/gui_adv_main.exe', ''.join([
        '../releases/v', VERSION, '/DataPreprocessingHelper-v', VERSION,
        '-', BIT, '/DataPreprocessingHelper.exe'
    ]))
    copy_tree('./StaticFiles/', ''.join([
        '../releases/v', VERSION, '/DataPreprocessingHelper-v', VERSION,
        '-', BIT, '/'
    ]))
    copyfile('../doc/UserManual.pdf', ''.join([
        '../releases/v', VERSION, '/DataPreprocessingHelper-v', VERSION,
        '-', BIT, '/UserManual.pdf'
    ]))
    copyfile(''.join(['../changelog/v', VERSION, '.txt']), ''.join([
        '../releases/v', VERSION, '/DataPreprocessingHelper-v', VERSION,
        '-', BIT, '/Changelog.txt'
    ]))

    # zip the files
    PATHNAME = ''.join([
        '../releases/v', VERSION, '/DataPreprocessingHelper-v', VERSION,
        '-', BIT
    ])
    ZIPFILENAME = ''.join([PATHNAME, '.zip'])
    with zipfile.ZipFile(ZIPFILENAME, 'w', zipfile.ZIP_DEFLATED) as fopened:
        # additional instruction to avoid zipping the directory
        abs_src = os.path.abspath(PATHNAME)
        for root, dirs, files in os.walk(PATHNAME):
            for file in files:
                absname = os.path.abspath(os.path.join(root, file))
                arcname = absname[len(abs_src) + 1:]
                fopened.write(absname, arcname)

    # clean all created files in the current directory
    os.remove('./gui_adv_main.spec')
    rmtree('./build/')
    rmtree('./dist/')
