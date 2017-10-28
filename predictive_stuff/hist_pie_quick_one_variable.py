import pandas, numpy, math, json
from matplotlib import pyplot
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import pylab, time
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

delay = actual_time_col - planned_time_col

delay_minutes = []
for i in range(len(delay)):
    temp = abs((delay[i] / numpy.timedelta64(1, 's')) / 60)
    delay_minutes.append(temp)

print min(delay_minutes)
print max(delay_minutes)

print np.nanmean(delay_minutes)
print np.nanmedian(delay_minutes)
#print median(delay_minutes)
time.sleep(5)

hist_len = 10000

temp = []
for i in range(len(delay_minutes)):
    if delay_minutes[i] < hist_len:
        temp.append(delay_minutes[i])

bins = np.arange(0, 1000, 1)

pie_plot = 0
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