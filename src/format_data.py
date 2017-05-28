#!/usr/bin/python3
"""
    This file contains functions that format data to convert time-of-change
    data to data acquired at fixed intervals

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/04/11
    License of the source code: MIT license
"""

# import python internal libraries
from datetime import datetime, timedelta
from math import isnan
from ntpath import split
from os import mkdir
from os.path import dirname
from pathlib import Path

# import third party libraries
from pandas import DataFrame, ExcelWriter, to_numeric

# import user-defined libraries


# write functions
def convert_df(datadfs: dict, start_time: datetime=None,
               end_time: datetime=None, interval: float=600,
               step: bool=True, ini_val: int=1,
               output_file: str=None, sep: str=';',
               output_timestring: str='%Y/%m/%d %H:%M:%S',
               outputtimevalue: str='None') -> dict:
    """
        This function converts a dataframe which data are converted according
        to time of change of values to data collected at fixed intervals.
        Return a dict of pandas DataFrame collected at fixed intervals with
        key values being the name of the worksheets. If a column
        contains no valid values, it returns a column of NaN values instead.

        Inputs:
        ==========
        datadfs: dict of pandas DataFrame
            dict of pandas DataFrame which index are datetime.datetime objects
            and contain data collected at time of change

        start_time: datetime.datetime
            user-defined starting time. If none is input, use the first
            datetime given in the datadf

        end_time: datatime.datetime
            users preliminary override of the ending time of the new
            dataframe. If it does not fit the intervals correctly, it may
            get updated

        interval: float
            user-defined time interval for the new data frame in seconds.
            Default 600 (10 minutes)

        step: bool
            if the data should be considered to be step functions. Default
            True. Indeed this input won't work until further notice.

        ini_val: int
            the assumption to the initial value of a column if the start time
            is before the occurrence of the initial value in the column.
                1: Use the minimum value in the trend
                2: Use the first value in the trend
                3: Fill in float('nan') (blank) values
            Default 1

        output_file: str
            the path where the dataframe should be output as a csv, xls
            or xlsx depending on the extension. Default None: no output

        sep: str
            separator in the csv. Default ';'

        output_timestring: str
            format time string in the output file. Default '%Y-%m-%d %H:%M:%S'

        outputtimevalue: str
            format time string into values from the user-defined start time.
            Default 'None'. Can be 'seconds', 'minutes', 'hours' and 'days'
    """

    final_dfs = {}
    for sheet_name in datadfs:
        datadf = datadfs[sheet_name]
        if start_time is None:
            start_time = datadf.index[0]  # intialize it with the dataframe

        # calculate the ending index for the new dataframe
        num = 1
        if end_time is None:
            while start_time+timedelta(seconds=interval*num) < \
                    datadf.index[-1]:
                num += 1
        else:
            while start_time+timedelta(seconds=interval*num) < end_time:
                num += 1
        end_time = start_time+timedelta(seconds=interval*num)

        # create the new dataframe with the correct indexes and column names
        final_df = DataFrame(index=[
            start_time+timedelta(seconds=interval*ind) for ind in range(num+1)
        ], columns=datadf.columns)

        # calculate the starting values for the new dataframe
        # if the starting value is not given, assume that the initial value
        # is the smallest for all possible values
        ini_val_pos = []  # locations of the initial good values
        sec_val_pos = []  # locations of the second good values
        final_df_inis = []  # location of initial value in new dataframe
        for col in final_df.columns:
            # # if the whole column is nan, skip the loop immediately
            # if all([
                    # isinstance(ent, str) or isnan(ent)
                    # for ent in datadf.loc[
                        # start_time:end_time+timedelta(0, 0, 1), col
                    # ]  # include the one at end_time
                    # ]):
                # final_df.loc[:, col] = float('nan')
                # ini_val_pos.append(datadf.shape[0])
                # continue  # next loop
            # find the appearance of the first value
            # initialize the position for data that contain no good values
            # should be the index right before the start time of the new
            # dataframe
            pos = datadf.index[-1]
            sec_pos = datadf.index[-1]
            num_gd_value = 0  # number of good values indexed
            for ind_oldind, oldind in enumerate(datadf.index[:-1]):
                if not isinstance(datadf.loc[oldind, col], str) and \
                        not isnan(datadf.loc[oldind, col]) and \
                        datadf.index[ind_oldind+1] > final_df.index[0] and \
                        num_gd_value == 0:
                    pos = oldind
                    ini_val_pos.append(ind_oldind)
                    num_gd_value = 1
                elif not isinstance(datadf.loc[oldind, col], str) and \
                        not isnan(datadf.loc[oldind, col]) and \
                        num_gd_value == 1:
                    sec_pos = oldind
                    sec_val_pos.append(ind_oldind)
                    num_gd_value = 2
                    break
            # fill in placeholders if not collected
            if num_gd_value == 0:
                ini_val_pos.append(datadf.shape[0]-1)
            if num_gd_value <= 1:
                sec_val_pos.append(datadf.shape[0]-1)
            # assign first value
            final_df_ini = 0
            # shift the final_df initial index if nan values are needed
            if ini_val == 3:
                while final_df_ini < final_df.shape[0]-1 and \
                        final_df.index[final_df_ini] < pos:
                    final_df.loc[final_df.index[final_df_ini], col] = \
                        float('nan')
                    final_df_ini += 1
            if pos > final_df.index[-1] or num_gd_value == 0:
                # if the first good value appears after the ending time
                # or there are no good values in the trend
                final_df.loc[:, col] = float('nan')
            elif final_df.index[final_df_ini] >= pos or ini_val == 2:
                # if the first value in the new frame may be the same as that
                # of the old one
                if final_df.index[final_df_ini] == pos or step or (
                        ini_val == 2 and final_df.index[final_df_ini] < pos
                        ):
                    # when the first value in the column equals to the first
                    # available value
                    final_df.loc[final_df.index[final_df_ini], col] = \
                        datadf.loc[pos, col]
                else:  # need interpolation
                    final_df.loc[final_df.index[final_df_ini], col] = \
                        interpolate_with_s(
                            final_df.index[final_df_ini], pos, sec_pos,
                            datadf.loc[pos, col], datadf.loc[sec_pos, col]
                        )
            else:
                # the minimum value assumption should be used
                # use to_numeric to push all non-numeric data to NaN values
                try:
                    final_df.loc[final_df.index[0], col] = to_numeric(
                        datadf[col][start_time:end_time+timedelta(0, 0, 1)],
                        errors='coerce'
                    ).dropna().unique().min()  # include the one at end_time
                except ValueError:  # no valid values
                    final_df.loc[:, col] = float('nan')
            final_df_ini += 1
            final_df_inis.append(final_df_ini)

        if step:  # assume step function
            # continue to append new columns until the end
            for col, ini, new_ini in zip(
                    final_df.columns, ini_val_pos, final_df_inis
                    ):
                # if the whole column is nan value, skip the col
                if all([
                        isinstance(ent, str) or isnan(ent)
                        for ent in datadf.loc[
                            start_time:end_time+timedelta(0, 0, 1), col
                        ]  # include the one at end_time
                        ]):
                    continue # skip column
                oldind = ini
                newind = new_ini
                oldlen = datadf.shape[0]
                newlen = final_df.shape[0]
                while newind < newlen:
                    if final_df.index[newind] < datadf.index[oldind]:
                        # use the previous value
                        final_df.loc[final_df.index[newind], col] = \
                            final_df.loc[final_df.index[newind-1], col]
                    else:
                        # find a new value
                        if isinstance(
                                datadf.loc[datadf.index[oldind], col], str
                                ) or isnan(
                                    datadf.loc[datadf.index[oldind], col]
                                ):
                            final_df.loc[final_df.index[newind], col] = \
                                final_df.loc[final_df.index[newind-1], col]
                        else:
                            final_df.loc[final_df.index[newind], col] = \
                                datadf.loc[datadf.index[oldind], col]
                        if oldind < oldlen-1:
                            oldind += 1
                    newind += 1
        else:  # run interpolation
            # continue to append new columns until the end
            newlen = final_df.shape[0]
            for col, ini, new_ini in zip(
                    final_df.columns, ini_val_pos, final_df_inis
                    ):
                newind = new_ini
                # to fit the initial value assumption
                try:
                    while final_df.index[newind] < datadf.index[ini]:
                        final_df.loc[final_df.index[newind], col] = \
                            final_df.loc[final_df.index[newind-1], col]
                        newind += 1
                except IndexError:  # all initial values
                    continue  # next loop
                oldind = ini
                while newind < newlen:
                    # find the next available value in the old dataframe
                    oldoldind = oldind
                    oldind += 1
                    try:
                        while isinstance(
                                datadf.loc[datadf.index[oldind], col], str
                                ) or isnan(
                                    datadf.loc[datadf.index[oldind], col]
                                ):
                            oldind += 1
                    except IndexError:  # out of frame. Use the old value
                        oldind = oldoldind
                    # for both interpolation and extrapolation at the end
                    while newind < newlen and (
                            oldind == oldoldind or
                            final_df.index[newind] <= datadf.index[oldind]
                            ):
                        if oldind == oldoldind:  # extrapolation at the end
                            final_df.loc[final_df.index[newind], col] = \
                                interpolate_with_s(
                                    final_df.index[newind],
                                    datadf.index[oldind-1],
                                    datadf.index[oldind],
                                    datadf.loc[datadf.index[oldind-1], col],
                                    datadf.loc[datadf.index[oldind], col]
                                )
                        else:
                            # interpolation
                            final_df.loc[final_df.index[newind], col] = \
                                interpolate_with_s(
                                    final_df.index[newind],
                                    final_df.index[newind-1],
                                    datadf.index[oldind],
                                    final_df.loc[final_df.index[newind-1], col],
                                    datadf.loc[datadf.index[oldind], col]
                                )
                        newind += 1

        # change time format as needed
        if outputtimevalue != 'None':
            coltime = ''.join(['TimeValue from ', str(final_df.index[0])])
            final_df.loc[:, coltime] = (
                final_df.index-final_df.index[0]
            ).total_seconds()
            if outputtimevalue == 'minutes':
                final_df.loc[:, coltime] = \
                    final_df.loc[:, coltime]/60.0
            elif outputtimevalue == 'hours':
                final_df.loc[:, coltime] = \
                    final_df.loc[:, coltime]/3600.0
            elif outputtimevalue == 'days':
                final_df.loc[:, coltime] = \
                    final_df.loc[:, coltime]/3600.0/24.0
            final_df.set_index(coltime, inplace=True)

        final_dfs[sheet_name] = final_df

    # output new file
    if output_file is not None:
        mkdir_if_not_exist(dirname(output_file))
        if output_file.split('.')[-1] == 'csv':
            final_dfs[[ent for ent in final_dfs.keys()][0]].to_csv(
                output_file, sep=sep, date_format=output_timestring
            )
        elif output_file.split('.')[-1] == 'xlsx':
            # need to open and close files if engine is not 'xlsxWriter'
            with ExcelWriter(
                    output_file, engine='xlsxwriter'
                    ) as writer:
                for ind, sheet_name in enumerate(final_dfs):
                    if len(sheet_name) < 30:
                        final_dfs[sheet_name].to_excel(writer, sheet_name)
                    else:  # limit to excel worksheet name
                        final_dfs[sheet_name].to_excel(writer, ''.join([
                            sheet_name[0:27], '(', '%02i' % (ind+1), ')'
                        ]))
                writer.save()
        elif output_file.split('.')[-1] == 'xls':
            with ExcelWriter(
                    output_file, engine='xlwt'
                    ) as writer:
                for sheet_name in final_dfs:
                    if len(sheet_name) < 30:
                        final_dfs[sheet_name].to_excel(writer, sheet_name)
                    else:  # limit to excel worksheet name
                        final_dfs[sheet_name].to_excel(writer, ''.join([
                            sheet_name[0:27], '(', '%02i' % (ind+1), ')'
                        ]))
                writer.save()
        else:
            raise ValueError('Wrong extension for output file')

    return final_dfs


def mkdir_if_not_exist(usrpath: str):
    """
        Make a directory at usrpath if the directory does not exist

        Inputs:
        ==========
        usrpath: str
            position of the path
    """

    if not Path(usrpath).exists():
        mkdir(usrpath)


def interpolate_with_s(mid_date: datetime, a_date: datetime, b_date: datetime,
                       aval: float, bval: float) -> float:
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

        aval: float
            value a

        bval: float
            value b
    """
    # use total seconds for large diff
    try:
        result = (bval-aval)*(mid_date-a_date).total_seconds() /\
            (b_date-a_date).total_seconds()+aval
    except TypeError:
        return float('nan')
    return result

# testing functions
if __name__ == '__main__':

    from os.path import basename
    from os import remove
    from data_read import read_data

    from pandas import read_csv, read_excel, Timestamp, ExcelFile

    # check for assuming nan values for data before the first valid value
    FILENAME = '../dat/time_of_change.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 6, 0), datetime(2017, 1, 3, 10, 0),
        ini_val=3
    )
    assert isnan(
        NEW_DFS['time_of_change'].loc[datetime(2017, 1, 3, 9, 50), 'Item 2']
    )
    assert NEW_DFS['time_of_change'].loc[
        datetime(2017, 1, 3, 10, 0), 'Item 2'
    ] == 1
    assert isnan(
        NEW_DFS['time_of_change'].loc[datetime(2017, 1, 1, 6, 30), 'Item 3']
    )
    assert NEW_DFS['time_of_change'].loc[
        datetime(2017, 1, 1, 9, 40), 'Item 3'
    ] == 1
    assert isnan(
        NEW_DFS['time_of_change'].loc[datetime(2017, 1, 1, 6, 30), 'Item 4']
    )

    # test the interpolation abilities for the first value
    FILENAME = '../dat/missing_data_altered.xls'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 11, 30), datetime(2017, 1, 1, 22, 00),
        ini_val=2, step=False
    )
    NEW_DF = NEW_DFS['Sheet1']
    assert NEW_DF.loc[datetime(2017, 1, 1, 11, 30), 'Pressure'] == 4.5

    # check the end time
    FILENAME = '../dat/time_of_change.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 2, 0, 0), ini_val=1
    )
    assert NEW_DFS['time_of_change'].index[-1] == datetime(2017, 1, 7, 22, 30)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 2, 0, 0), datetime(2017, 1, 2, 10, 0)
    )
    assert NEW_DFS['time_of_change'].index[-1] == datetime(2017, 1, 2, 10, 0)

    # check for formatting with intermediate beginning time step
    FILENAME = '../dat/time_of_change.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 2, 0, 0), datetime(2017, 1, 3, 0, 0)
    )
    assert isnan(
        NEW_DFS['time_of_change'].loc[datetime(2017, 1, 2, 9, 30), 'Item 1']
    )
    assert NEW_DFS['time_of_change'].loc[
        datetime(2017, 1, 2, 10, 40), 'Item 3'
    ] == 1
    assert NEW_DFS['time_of_change'].loc[
        datetime(2017, 1, 2, 1, 0), 'Item 3'
    ] == 0
    assert NEW_DFS['time_of_change'].loc[
        datetime(2017, 1, 2, 6, 0), 'Item 4'
    ] == 1

    # check for interpolation for consecutive invalid values
    FILENAME = '../dat/missing_data.xls'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(TEST_DFS, step=False)
    assert NEW_DFS['Sheet1'].loc[
        datetime(2017, 1, 1, 11, 10), 'Pressure'
    ] == 2
    assert NEW_DFS['Sheet1'].loc[
        datetime(2017, 1, 1, 11, 20), 'Pressure'
    ] == 3
    assert isnan(NEW_DFS['Sheet1'].loc[
        datetime(2017, 1, 1, 11, 20), 'Cost'
    ])
    assert isnan(NEW_DFS['Sheet1'].loc[
        datetime(2017, 1, 1, 11, 20), 'Price'
    ])

    # check super long name file output
    FILENAME = \
        '../dat/time_of_change-long-name-file-0123456789001234567890.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(TEST_DFS, output_file='./testresult.xlsx')
    remove('./testresult.xlsx')   

    # check time output
    # check function for computer-generated ending time
    FILENAME = '../dat/time_of_change.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), outputtimevalue='seconds'
    )
    assert isinstance(NEW_DFS['time_of_change'].index[0], float)
    FILENAME = '../dat/missing_data.xlsx'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), outputtimevalue='days'
    )
    assert isinstance(NEW_DFS['Sheet1'].index[0], float)

    # test the writing of multiple sheets
    FILENAME = '../dat/missing_data.xlsx'
    TEST_DFS = read_data(FILENAME, header=0, sheetnames=[])
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 11, 0), datetime(2017, 1, 1, 22, 00),
        ini_val=2, step=False, output_file='./testresult.xlsx'
    )
    with ExcelFile('./testresult.xlsx') as xlsx:
        assert len(xlsx.sheet_names) == 3
        for sheet_name in xlsx.sheet_names:
            assert sheet_name in NEW_DFS.keys()
    remove('./testresult.xlsx')
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 11, 0), datetime(2017, 1, 1, 22, 00),
        ini_val=2, step=False, output_file='./testresult.xls'
    )
    with ExcelFile('./testresult.xls') as xlsx:
        assert len(xlsx.sheet_names) == 3
        for sheet_name in xlsx.sheet_names:
            assert sheet_name in NEW_DFS.keys()
    remove('./testresult.xls')

    # check function for no start_time
    FILENAME = '../dat/time_of_change-trimmed.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(TEST_DFS)
    assert isinstance(NEW_DFS['time_of_change-trimmed'], DataFrame)
    # same index in the beginning?
    assert NEW_DFS['time_of_change-trimmed'].index[0] == \
        TEST_DFS['time_of_change-trimmed'].index[0]

    # check what happen to data that contain no good values
    FILENAME = '../dat/time_of_change-trimmed.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(TEST_DFS, datetime(2017, 1, 1, 0, 0))
    assert isinstance(NEW_DFS['time_of_change-trimmed'], DataFrame)
    # keeping the invalid values
    assert len(
        NEW_DFS['time_of_change-trimmed'].loc[:, 'Item 1'].dropna()
    ) == 0

    # check function for computer-generated ending time
    FILENAME = '../dat/time_of_change.csv'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(TEST_DFS, datetime(2017, 1, 1, 0, 0))
    assert isinstance(NEW_DFS['time_of_change'], DataFrame)
    assert NEW_DFS['time_of_change'].index[-1] >= \
        TEST_DFS['time_of_change'].index[-1]
    assert NEW_DFS['time_of_change'].index[-2] <= \
        TEST_DFS['time_of_change'].index[-1]

    # check function for new ending time
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), datetime(2017, 1, 3, 11, 50),
        output_file='./testresult.csv'
    )
    assert Path('./testresult.csv').exists()
    remove('./testresult.csv')
    NEW_DF = NEW_DFS['time_of_change']
    assert NEW_DF.index[-1] == datetime(2017, 1, 3, 11, 50)
    assert NEW_DF.loc[NEW_DF.index[0], 'Item 4'] == 0.0
    assert NEW_DF.loc[NEW_DF.index[0], 'Item 3'] == 0.0
    # check function of the correction
    assert isnan(NEW_DF.loc[datetime(2017, 1, 3, 10, 50), 'Item 1'])
    assert NEW_DF.loc[datetime(2017, 1, 3, 10, 50), 'Item 2'] == 1.0
    assert NEW_DF.loc[datetime(2017, 1, 3, 10, 50), 'Item 3'] == 0.0
    assert NEW_DF.loc[datetime(2017, 1, 3, 10, 50), 'Item 4'] == 0.0

    # check function with new initial values
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), datetime(2017, 1, 3, 11, 50),
        ini_val=2
    )
    NEW_DF = NEW_DFS['time_of_change']
    # check function of the correction
    assert isnan(NEW_DF.loc[datetime(2017, 1, 1, 0, 0), 'Item 1'])
    assert NEW_DF.loc[datetime(2017, 1, 1, 0, 0), 'Item 2'] == 1.0
    assert NEW_DF.loc[datetime(2017, 1, 1, 0, 0), 'Item 3'] == 1.0
    assert NEW_DF.loc[datetime(2017, 1, 1, 0, 0), 'Item 4'] == 0.0

    # check function of the interpolation
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), datetime(2017, 1, 3, 11, 50),
        ini_val=2, step=False
    )
    NEW_DF = NEW_DFS['time_of_change']
    assert NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 2'] <= 1.0
    assert NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 3'] <= 1.0
    assert NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 4'] <= 1.0
    assert isnan(NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 1'])
    assert NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 2'] > 0.0
    assert NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 3'] > 0.0
    assert NEW_DF.loc[datetime(2017, 1, 3, 11, 50), 'Item 4'] > 0.0

    # check output file
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), datetime(2017, 1, 3, 11, 50),
        ini_val=2, output_file='./testresult.xls'
    )
    assert Path('./testresult.xls').exists()
    remove('./testresult.xls')
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 0, 0), datetime(2017, 1, 3, 11, 50),
        ini_val=2, output_file='./testresult.xlsx'
    )
    assert Path('./testresult.xlsx').exists()
    remove('./testresult.xlsx')

    # check time string
    for filename in [
        './testresult.csv', './testresult.xlsx', './testresult.xls'
    ]:
        NEW_DFS = convert_df(
            TEST_DFS, datetime(2017, 1, 1, 0, 0), datetime(2017, 1, 1, 11, 50),
            ini_val=2, output_file=filename
        )
        if 'csv' in filename:
            NEW_DFS = read_csv(
                filename, sep=';', index_col=0, parse_dates=True,
                infer_datetime_format='%Y/%m/%d %H:%M:%S'
            )
        else:
            NEW_DFS = read_excel(filename)
        assert isinstance(
            NEW_DFS[[ent for ent in NEW_DFS.keys()][0]].index[0], Timestamp
        )
        remove(filename)

    # test the interpolation abilities
    FILENAME = '../dat/missing_data.xls'
    TEST_DFS = read_data(FILENAME, header=0)
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 11, 0), datetime(2017, 1, 1, 22, 00),
        ini_val=2, step=False
    )
    NEW_DF = NEW_DFS['Sheet1']
    assert isinstance(
        NEW_DF.loc[datetime(2017, 1, 1, 12, 0), 'Pressure'], float
    )
    assert NEW_DF.loc[datetime(2017, 1, 1, 22, 0), 'Pressure'] != 0.0
    assert NEW_DF.loc[datetime(2017, 1, 1, 12, 0), 'Pressure'] == (
        TEST_DFS['Sheet1'].loc[datetime(2017, 1, 1, 11, 50), 'Pressure'] +
        TEST_DFS['Sheet1'].loc[datetime(2017, 1, 1, 12, 10), 'Pressure']
    )/2.0

    # test the covert_df function for minimum initial values when string
    # characters are involved
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 10, 0), datetime(2017, 1, 1, 22, 00),
        ini_val=1, step=False
    )

    # test the covert_df function for step function with string characters
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 10, 0), datetime(2017, 1, 1, 22, 00),
        ini_val=2, step=True
    )
    NEW_DFS = convert_df(
        TEST_DFS, datetime(2017, 1, 1, 10, 0), datetime(2017, 1, 1, 22, 00),
        ini_val=1, step=True
    )

    print('All functions in', basename(__file__), 'are ok')
