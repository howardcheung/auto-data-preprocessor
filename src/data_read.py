#!/usr/bin/python3
"""
    This file contains functions that read data in xlsx format. They also
    preprocess the data and wrap them into a namedtuple.

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/04/11
    License of the source code: MIT license
"""

# import python internal libraries
from datetime import datetime
from math import isnan
from ntpath import split

# import third party libraries
# from numpy import where
from pandas import DataFrame, Series, ExcelFile, read_csv, read_excel
from pandas.tslib import Timestamp

# import user-defined libraries


# write functions
def read_data(filename: str, header: int=None,
              time_format: str='%m/%d/%y %I:%M:%S %p CST',
              sheetnames: list=None,
              interpolation: bool=False, duration: bool=False) -> dict:
    """
        This function reads the data in filename that is in specified format
        and returns a pandas dataframe with time data as the index and
        'CLG' as the header of the cooling load data. The final dataframe
        contains 'CLG' as the cooling load data column and 'Duration' as the
        duration of each data point in seconds. Since the file may be an xls
        file that contains multiple worksheets, the final returned result
        is a python dict object with key values being the sheet names and dict
        values being the dataframes.

        Inputs:
        ==========
        filename: string
            path to the data file

        header: int, list of ints, default None
            Row (0-indexed) to use for the column labels of the parsed
            DataFrame. If a list of integers is passed those row positions
            will be combined into a MultiIndex. Default None

        time_format: string
            format of string in time. Default '%m/%d/%y %I:%M:%S %p CST'
            Please check https://docs.python.org/3.5/library/datetime.html#strftime-and-strptime-behavior
            for details

        sheetnames: list
            list of string for the name of worksheets to be imported. Default
            None which means that only the first sheet will be imported

        interpolation: bool
            if the code should conduct an interpolation for values that are
            NaN in the sheet. Default False

        duration: bool
            if the code should calculate the duration of each point in the
            time series and create a new column called 'Duration' in
            seconds. Default False
    """

    # initialize the dataframe
    ext = filename.split('.')[-1]

    # preprocess pddf time string
    def _time_config(pddf):
        """
            Preprocess the time string in a pandas DataFrame and returns
            a pandas DataFrame
        """

        # rename the first column name
        pddf.columns = ['Time']+pddf.columns.tolist()[1:]

        # make time column as the index
        try:
            pddf.loc[:, 'Time'] = [
                datetime.strptime(timestr, time_format)
                for timestr in pddf.loc[:, 'Time']
            ]
        except TypeError:  # the time string has been converted by pandas
            pass
        pddf.set_index('Time', inplace=True)

        return pddf

    # read the file. Read the file as two columns first to conduct
    # preprocessing before
    pddfs = {}
    if ext == 'xlsx' or ext == 'xls':
        with ExcelFile(filename) as xlsx:
            if sheetnames is None:
                for sheet_name in xlsx.sheet_names:
                    pddfs[sheet_name] = _time_config(read_excel(
                        xlsx, sheet_name, header=header
                    ))
                    break  # read first sheet
            else:
                for sheet_name in sheetnames:
                    pddfs[sheet_name] = _time_config(read_excel(
                        xlsx, sheet_name, header=header
                    ))  # read the specified sheets
    elif ext == 'csv':
        pddf = read_csv(filename, header=header)
        if pddf.shape[1] == 1:
            # one column only including the index. The separator is wrong.
            pddf = read_csv(filename, header=header, sep=';')
        if pddf.shape[1] == 1:
            # one column only including the index. The separator is wrong.
            pddf = read_csv(filename, header=header, sep='\t')
        # use the name of the file as the worksheet name
        pddfs[split(filename)[-1].split('.')[0]] = _time_config(pddf)
    else:
        raise ValueError(''.join([
            'The file extension of the data file cannot be recognized by ',
            'data_read.read_data(). Exiting.......'
        ]))

    # not using numpy for license issue
    # # preprocessing by interpolating invalid columns
    # if interpolation:
        # for col in pddf.columns:
            # pddf.loc[:, col] = check_nan(pddf[col])

    # # calculate the duration of each data point
    # if duration:
        # pddf.loc[:, 'Duration'] = [
            # cal_each_duration(ind, timeind, pddf[pddf.columns[0]])
            # for ind, timeind in enumerate(pddf[pddf.columns[0]].index)
        # ]

    return pddfs


def interpolate_with_s(mid_date: datetime, a_date: datetime, b_date: datetime,
                       a_value: float, b_value: float) -> float:
    """
        Interpolate with datetime.datetime objects bewteen values a and b on
        two different dates based on their difference in seconds

        Inputs:
        ==========
        mid_date: datetime.datetime
            the date where the value is needed

        a_date: datetime.datetime
            the date where value a is

        b_date: datetime.datetime
            the date where value b is

        a_value: float
            value a

        b_value: float
            value b
    """

    return (b_value-a_value)*(mid_date-a_date).seconds /\
        (b_date-a_date).seconds+a_value


# def check_nan(wseries: Series) -> Series:
    # """
        # This function checks the values inside the series. If any of them
        # are nan or str, user interpolation with adjacent values to
        # substitute it. Returns the corrected Series

        # Inputs:
        # ==========
        # wseries: Series
            # pandas Series data with values in float and index as
            # datetime.datetime object
    # """

    # if len(wseries[Series([(
            # isinstance(val, str) or isnan(val)
        # ) for val in wseries], index=wseries.index)]) == 0:
        # return wseries  # nothing to change

    # # ensure that all are either float or nan
    # def _float_or_nan(ent):
        # """
            # Force values to be either a float or nan first
        # """
        # try:
            # return float(ent)
        # except ValueError:
            # return float('nan')

    # wseries = Series(
        # [_float_or_nan(val) for val in wseries], index=wseries.index,
        # name=wseries.name
    # )

    # # continue with interpolation or extrapolation if needed
    # inds = where(
        # Series([
            # (isinstance(val, str) or isnan(val)) for val in wseries
        # ], index=wseries.index)
    # )[0]  # locate the position of the problematic readings
    # for ind in inds:
        # try:
            # wseries[ind] = interpolate_with_s(
                # wseries.index[ind], wseries.index[ind-1],
                # wseries.index[ind+1],
                # wseries[ind-1], wseries[ind+1]
            # )
            # if isnan(wseries[ind]):  # interpolation does not work
                # wseries[ind] = interpolate_with_s(
                    # wseries.index[ind], wseries.index[ind-2],
                    # wseries.index[ind-1],
                    # wseries[ind-2], wseries[ind-1]
                # )
        # except IndexError:  # extrapolation
            # try:
                # wseries[ind] = interpolate_with_s(
                    # wseries.index[ind], wseries.index[ind-2],
                    # wseries.index[ind-1],
                    # wseries[ind-2], wseries[ind-1]
                # )
            # except IndexError:
                # wseries[ind] = interpolate_with_s(
                    # wseries.index[ind], wseries.index[ind+2],
                    # wseries.index[ind+1],
                    # wseries[ind+2], wseries[ind+1]
                # )

    # return wseries


# def cal_each_duration(ind: int, timeind: Timestamp, wseries: Series) -> float:
    # """
        # This function calculates the duration for each data point in the time
        # series given by the acqusition interval of the data

        # Inputs:
        # ==========
        # ind: int
            # index number in the pandas Series

        # timeind: tslib.Timestamp
            # time stamp at the index being analyzed

        # wseries: Series
            # pandas Series data with values in float and index as
            # datetime.datetime object
    # """

    # length = len(wseries)
    # if ind == 0:
        # return (wseries.index[ind+1]-timeind).seconds
    # elif ind == length-1:
        # return (timeind-wseries.index[ind-1]).seconds
    # else:
        # return ((wseries.index[ind+1]-wseries.index[ind-1]).seconds)/2.0


# testing functions
if __name__ == '__main__':

    from os.path import basename

    # testing file reading with multiple worksheets
    FILENAME = '../dat/missing_data.xlsx'
    print('Testing file import by using ', FILENAME)
    TEST_DFS = read_data(FILENAME, header=0, sheetnames=['Sheet1', 'Sheet2'])
    import pdb; pdb.set_trace()
    assert TEST_DFS['Sheet1'].columns.tolist()[0] == 'Pressure'
    assert TEST_DFS['Sheet2'].columns.tolist()[1] == 'Cost'

    # testing import with dates
    FILENAME = '../dat/date.csv'
    print('Testing file import by using ', FILENAME)
    TEST_DF = read_data(
        FILENAME, header=0, time_format='%Y-%m-%d'
    )
    assert isinstance(TEST_DF['date'].index[0], Timestamp)

    FILENAME = '../dat/missing_data.xls'
    print('Testing file import by using ', FILENAME)
    TEST_DF = read_data(FILENAME, header=0, duration=True,
                        interpolation=True)
    assert isinstance(TEST_DF['Sheet1'].index[0], Timestamp)
    # assert TEST_DF.loc[TEST_DF.index[0], 'Duration'] == 60*30
    # assert TEST_DF.loc[TEST_DF.index[2], 'Duration'] == 60*30
    # assert TEST_DF.loc[TEST_DF.index[-1], 'Duration'] == 60*30

    for FILENAME in [
        '../dat/time_of_change-semicolon.csv',
        '../dat/time_of_change.csv'
    ]:
        print('Testing file import by using ', FILENAME)
        SHTNAME = split(FILENAME)[-1].split('.')[0]
        TEST_DF = read_data(FILENAME, header=0)[SHTNAME]
        assert isinstance(TEST_DF.index[0], Timestamp)
        assert isnan(TEST_DF.loc[TEST_DF.index[0], 'Item 1'])
        assert isnan(TEST_DF.loc[TEST_DF.index[1], 'Item 1'])
        assert TEST_DF.loc[TEST_DF.index[1], 'Item 3'] == 1.0
        assert isnan(TEST_DF.loc[TEST_DF.index[0], 'Item 3'])
        assert TEST_DF.loc[TEST_DF.index[0], 'Item 4'] == 0.0

    # test for multi-header
    FILENAME = '../dat/time_of_change_multiheader.csv'
    print('Testing file import by using ', FILENAME)
    SHTNAME = split(FILENAME)[-1].split('.')[0]
    TEST_DF = read_data(FILENAME, header=1)[SHTNAME]
    assert isinstance(TEST_DF.index[0], Timestamp)
    assert isnan(TEST_DF.loc[TEST_DF.index[0], 'Item 1'])
    assert isnan(TEST_DF.loc[TEST_DF.index[1], 'Item 1'])
    assert TEST_DF.loc[TEST_DF.index[1], 'Item 3'] == 1.0
    assert isnan(TEST_DF.loc[TEST_DF.index[0], 'Item 3'])
    assert TEST_DF.loc[TEST_DF.index[0], 'Item 4'] == 0.0

    print('All functions in', basename(__file__), 'are ok')
