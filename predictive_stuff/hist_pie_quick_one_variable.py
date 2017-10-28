# -*- coding: utf-8 -*-
# coding: utf-8

import pandas, numpy, math, json
from matplotlib import pyplot
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import pylab, time, string
from pandas import Series
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

from pylab import *

####################### read from json files and convert them into df
db_data = pandas.DataFrame.from_csv('input/db_data.csv', sep = ';', parse_dates = [4,5])

train_number_col = Series.tolist(db_data['ZUGEREIGNIS_ZUGNUMMER'])

train_number_unique = []
for i in train_number_col:
    if i not in train_number_unique:
        train_number_unique.append(i)

planned_time_col = db_data['ZUGEREIGNIS_SOLLZEIT']
actual_time_col = db_data['ZUGEREIGNIS_ISTZEIT']

using_list = 0
if using_list:

    delay = actual_time_col - planned_time_col
    delay_minutes = []
    for i in range(len(delay)):
        temp = abs((delay[i] / numpy.timedelta64(1, 's')) / 60)
        delay_minutes.append(temp)

    print 'minimum delay', min(delay_minutes)
    print 'maximum delay',max(delay_minutes)

    print 'mean of delay',np.nanmean(delay_minutes)
    print 'median of delay',np.nanmedian(delay_minutes)


    plot = 1
    if plot:
        hist_len = 10000

        temp = []
        for i in range(len(delay_minutes)):
            if delay_minutes[i] < hist_len:
                temp.append(delay_minutes[i])

        bins = np.arange(0, 1000, 1)

    pie_plot = 1
    if pie_plot:
        # make a square figure and axes
        figure(1, figsize=(12, 12))
        ax = axes([0.1, 0.1, 0.8, 0.8])

        # The slices will be ordered and plotted counter-clockwise.
        labels = 'delay = 0 min', 'delay = 1 min', 'delay = 2 min', 'delay = 3 min','delay = 4 min','delay = 5 min'
        fracs = np.histogram(temp, bins=bins)

        pie(fracs[0][0:6],
            autopct='%1.1f%%', labels= labels,startangle=90)
        # The default startangle is 0, which would start
        # the Frogs slice on the x-axis.  With startangle=90,
        # everything is rotated counter-clockwise by 90 degrees,
        # so the plotting starts on the positive y-axis.

        title('Distribution of train delays in minutes', bbox={'facecolor': '0.8', 'pad': 5})

        show()


    hist_plot = 1
    if hist_plot:

        ########################### 2D bar histogram for all the models########################
        pyplot.hist(temp,bins=bins,histtype='bar',rwidth=0.4, label='Servicing Dates Diff Distribution', color='b')
        pyplot.xlabel('train delay in minutes')
        pyplot.ylabel('Number of train trips')
        pyplot.title('Distribution of train delays in last 15 days')

        pyplot.show()


    big_delays = []
    for i in range(len(delay_minutes)):
        if delay_minutes[i] > 30:
            big_delays.append(delay_minutes[i])

    print 'total number of times big delays occurred in last 15 days in stuttgart: ',len(big_delays)
    print 'total number of times big delays occurred per day in stuttgart : ',len(big_delays) / 15
    print 'total number of times big delays occurred per hour in stuttgart : ',len(big_delays) / (15*12)


using_df = 1
if using_df:
    db_data['delay'] = actual_time_col - planned_time_col

    db_data['delay'] = (db_data['delay'].divide(numpy.timedelta64(1, 'm'))).abs()

    print 'minimum delay', min(db_data['delay'])
    print 'maximum delay',max(db_data['delay'])

    print 'mean of delay',np.nanmean(db_data['delay'])
    print 'median of delay',np.nanmedian(db_data['delay'])

    print 'total number of trips in last 15 days in stuttgart : ', len(db_data['delay'])

    db_data_more_than_30mins = pandas.DataFrame()
    db_data_more_than_30mins = db_data[(db_data['delay'] > 30) & (db_data['QUELLE_SENDER'] == 'Leitsystem')]

    print 'total number of trips in last 15 days in stuttgart with more than 30 mins delay : ', len(db_data_more_than_30mins['delay'])

    unique_train_list = []
    for i in Series.tolist(db_data_more_than_30mins['ZUGEREIGNIS_ZUGNUMMER']):
        if i not in unique_train_list:
            unique_train_list.append(i)

    for train_number in unique_train_list:
        db_train = pandas.DataFrame()
        db_train = db_data_more_than_30mins[db_data_more_than_30mins['ZUGEREIGNIS_ZUGNUMMER'] == train_number]

        db_train.to_csv('output/train_delay'+str(train_number)+'.csv')

        db_train = db_train.dropna()

        convert_to_json = 1
        if convert_to_json:
            result_json = []
            for i in range(db_train.shape[0]):
                row = db_train.iloc[i]
                newRow = {
                  "type": "Feature",
                  "geometry": {
                    "type": "Point",
                    "coordinates":[row['LAENGE'],row['BREITE']]
                  },
                  "properties": {
                    "name": "Train Delay",
                    "delay":row['delay']
                  }
                }
                result_json.append(newRow)

            print result_json

            filename = 'output/train_delay'+str(train_number)+'.json'
            with open(filename, 'w') as outfile:
                json.dump(result_json, outfile)



        plot = 0
        if plot:
            pyplot.xlabel('Timestamps')
            pyplot.ylabel('Train delays in minutes')
            plot_title = 'Train delays for train number '+str(train_number)+' going from '+str(db_train['NAME'][0])+' to '+str(db_train['NAME'][-1])

            printable = set(string.printable)
            plot_title = filter(lambda x: x in printable, plot_title)

            pyplot.title(plot_title)

            pyplot.plot(db_train['ZUGEREIGNIS_SOLLZEIT'],db_train['delay'],'ro')
            pyplot.show()

