# auto-data-preprocessor
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