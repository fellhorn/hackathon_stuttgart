# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 23:27:55 2017

@author: Ediz
"""

from datetime import datetime as dt
import csv
import numpy as np
import matplotlib.pyplot as plt
import json

def getData(filename):
#%%
    with open(filename, newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=';')
        total_data = [row for row in csv_data]
    header = total_data[0]
    data = total_data[1:][:]
    data = list(map(list, zip(*data)))
    return header, data        
  #%%          
def sortData(header, data):
    TRAIN_TYPE      = 0
    TRAIN_NUMBER     = 1
    STATION_EVENT   = 2
    TRAIN_EVENT     = 3
    PLANNED_TIME    = 4
    ACTUAL_TIME     = 5
    SOURCE_TRANSMITTER = 6
    INCOMING_TIME   = 7
    SERVICE_ID      = 8
    NAME            = 9 
    LONG            = 10
    LAT             = 11
    GEO             = 12
    column_dict = { TRAIN_TYPE: 'ZUGEREIGNIS_ZUGGATTUNG',
                    TRAIN_NUMBER: 'ZUGEREIGNIS_ZUGNUMMER',
                    STATION_EVENT: 'ZUGEREIGNIS_DS100',
                    TRAIN_EVENT: 'ZUGEREIGNIS_TYP',
                    PLANNED_TIME: 'ZUGEREIGNIS_SOLLZEIT',
                    ACTUAL_TIME: 'ZUGEREIGNIS_ISTZEIT',
                    SOURCE_TRANSMITTER: 'QUELLE_SENDER',
                    INCOMING_TIME: 'EINGANGSZEIT',
                    SERVICE_ID: 'SERVICE ID',
                    NAME: 'NAME',
                    LONG:'LAENGE',
                    LAT:'BREITE',
                    GEO:'geo'} 
    
    #sort data for one column and apply the sort indices on every column
    sort_indices = [jj[0] for jj in sorted(enumerate(data[TRAIN_NUMBER]), key=lambda x:x[1])]
    for col_index in range(len(header)):
        data[col_index] = [data[col_index][row_index] for row_index in sort_indices]
        
    #Extract data for TRAIN_NUMBER
    index_list = [0]
    value_prev = data[TRAIN_NUMBER][0]
    for row_index in range(len(data[TRAIN_NUMBER])):
        if data[TRAIN_NUMBER][row_index]==value_prev:
            continue
        else:
            index_list.extend([row_index])
        value_prev = data[TRAIN_NUMBER][row_index]
    
    data_tmp = []  
    for ii in range(len(index_list)-1):
        data_cut    =data[:]
        date_string =[]
        for col_index in range(len(header)):
            data_cut[col_index] = [data_cut[col_index][row_index] for row_index in range(index_list[ii],index_list[ii+1]) if data[GEO][row_index]!=''] 
        
        for row_index in range(len(data_cut[ACTUAL_TIME])):
            if data_cut[ACTUAL_TIME][row_index][0:10] + ' ' + data_cut[ACTUAL_TIME][row_index][11:19] != ' ':
                date_string.extend([dt.strptime(data_cut[ACTUAL_TIME][row_index][0:10] + ' ' + data_cut[ACTUAL_TIME][row_index][11:19], '%Y-%m-%d %H:%M:%S')])
            else:
                continue
        sort_indices = [jj[0] for jj in sorted(enumerate(date_string), key=lambda x:x[1])]
        
        for col_index in range(len(header)):    
            data_cut[col_index] = [data_cut[col_index][row_index] for row_index in sort_indices]
        
        data_cut[LONG] = list(map(float, data_cut[LONG]))
        data_cut[LAT] = list(map(float, data_cut[LAT]))
        data_tmp.append(data_cut)
        
    data = data_tmp[:]
    
    return data

def list2dict(header, data):
    TRAIN_TYPE      = 0
    TRAIN_NUMBER     = 1
    STATION_EVENT   = 2
    TRAIN_EVENT     = 3
    PLANNED_TIME    = 4
    ACTUAL_TIME     = 5
    SOURCE_TRANSMITTER = 6
    INCOMING_TIME   = 7
    SERVICE_ID      = 8
    NAME            = 9 
    LONG            = 10
    LAT             = 11
    GEO             = 12
      
    data_dict = {}
    for train_number in range(len(data)):
        delay_list = []
        for row_index in range(len(data[train_number][ACTUAL_TIME])):
            if data[train_number][ACTUAL_TIME][row_index][0:10] + ' ' + data[train_number][ACTUAL_TIME][row_index][11:19] != ' ':
                if data[train_number][PLANNED_TIME][row_index][0:10] + ' ' + data[train_number][PLANNED_TIME][row_index][11:19] != ' ':
                    delay_time = dt.strptime(data[train_number][ACTUAL_TIME][row_index][0:10] + ' ' + data[train_number][ACTUAL_TIME][row_index][11:19], '%Y-%m-%d %H:%M:%S')-dt.strptime(data[train_number][PLANNED_TIME][row_index][0:10] + ' ' + data[train_number][PLANNED_TIME][row_index][11:19], '%Y-%m-%d %H:%M:%S')
                    delay_list.append(delay_time.total_seconds())
        data_dict[train_number] = {'TRAIN_NUMBER': data[train_number][TRAIN_NUMBER][0], 'PLANNED_TIME': data[train_number][PLANNED_TIME], 'ACTUAL_TIME': data[train_number][ACTUAL_TIME], 'DELAY_TIME': delay_list, 'LATITUDE': data[train_number][LAT], 'LONGITUDE': data[train_number][LONG]}
    
    return data_dict
    
def dict2json(data_dict):
    with open('db_data.json', 'w') as json_file:
        json.dump(data_dict, json_file)

if __name__ == '__main__':
    train_header, train_data = getData('db_data.csv')
    train_data = sortData(train_header, train_data)
    train_dict = list2dict(train_header, train_data)
    dict2json(train_dict)
    
#    fig, ax = plt.subplots()
#    ax.scatter(train_data[10], train_data[11])
#    for i, txt in enumerate(train_data[4]):
#        ax.annotate(txt[11:19], (train_data[10][i], train_data[11][i]))
    
         