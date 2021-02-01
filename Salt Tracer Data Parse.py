# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:47:30 2020

@author: IHiggins
"""

import pandas as pd

from tkinter import *   ## notice lowercase 't' in tkinter here
from tkinter import filedialog
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import subprocess, sys
from scipy.signal import find_peaks, chirp, peak_widths
import matplotlib.pyplot as plt
Tk().withdraw()
filename_upper = filedialog.askopenfilename(initialdir = "W:\STS\hydro\GAUGE\Temp\Ian's Temp\Raw Salt tracer data", title="Select Upper:", filetypes = (("CSV files","*.csv"),("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file

upper = pd.read_csv(filename_upper, header=None, skiprows=[0,1,2,3], usecols=[0,1,3])
print(upper)
#upper = pd.read_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Raw Salt tracer data\1_3_UPPE.txt",header=None, skiprows=[0,1,2,3], usecols=[0,1,3])
print(upper)
upper.columns = ['Date', 'Time', 'Upper ms/cm']

upper['Date_Time'] = pd.to_datetime(upper['Date'] + ' ' + upper['Time'])

upper['Date_Time'] = pd.to_datetime(upper['Date_Time'])
#upper.set_index('Date_Time',inplace=True)

Tk().withdraw()
filename_lower = filedialog.askopenfilename(initialdir = "W:\STS\hydro\GAUGE\Temp\Ian's Temp\Raw Salt tracer data", title="Select Lower:", filetypes = (("CSV files","*.csv"),("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file

lower = pd.read_csv(filename_lower, header=None, skiprows=[0,1,2,3], usecols=[0,1,3])
print("LOWER")
print(lower)
#lower = pd.read_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Raw Salt tracer data\1_3_2020.txt",header=None, skiprows=[0,1,2,3], usecols=[0,1,3])

lower.columns = ['Date', 'Time', 'Lower ms/cm']
print("LOWER")
print(lower)
lower['Date_Time'] = pd.to_datetime(lower['Date'] + ' ' + lower['Time'])
lower['Date_Time'] = pd.to_datetime(lower['Date_Time'])


dataA = upper.merge(lower, left_on=["Date_Time"], right_on=["Date_Time"]).fillna(method='ffill')

data = dataA[['Date_x','Time_x','Upper ms/cm', 'Lower ms/cm']].copy()

data.columns = ['Date', 'Time', 'Upper ms/cm', 'Lower ms/cm']


data.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\data.csv")
pd.to_datetime(data['Time'])
data['Date_Time'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

data['Date_Time'] = pd.to_datetime(data['Date_Time'])

data.set_index('Time', inplace=True)

data.sort_index(inplace=True)

df1 = data.loc['14:30:00':'16:00:00', :]

df1.reset_index(inplace=True)
print(df1)

def peak_calc():
###### UPPER ######################
    x_upper=df1.iloc[:,COLUMN]
    x_upper=np.array(x_upper)
    #peaks, _ = find_peaks(x_upper, height=0)
    peaks, properties = find_peaks(x_upper, prominence=(.01, None))

    width = peak_widths(x_upper, peaks)

    plt.show()    

    plt.plot(x_upper)
    plt.plot(peaks, x_upper[peaks], "x")
    plt.plot(np.zeros_like(x_upper), "--", color="gray")
    print("PEAK COUNT")
    print(peaks.size)

    arrival = width[2].round()
    ARRIVAL = df1['Date_Time'].loc[arrival]-df1['Date_Time'].loc[0]
    ARRIVAL = ARRIVAL.dt.total_seconds()
    ARRIVAL = ARRIVAL/60
    background = df1[SONDE].loc[arrival-1]
    peak_conductivity = df1[SONDE].max()
    peak_conductivty_calc = df1[SONDE].loc[peaks]
    PEAK=df1['Date_Time'].loc[peaks]-df1['Date_Time'].loc[0]
    PEAK = PEAK.dt.total_seconds()
    PEAK = PEAK/60
    flush = width[3].round()
    FLUSH = df1['Date_Time'].loc[flush]-df1['Date_Time'].loc[0]
    FLUSH = FLUSH.dt.total_seconds()
    FLUSH = FLUSH/60
    peak_size = float(FLUSH)-float(ARRIVAL)
    print("MAX CONDUCTIVITY: "+str(round(float(peak_conductivity),3))+" CALCULATED MAX: "+str(round(float(peak_conductivty_calc),3)))
    print(SONDE)
    print("BACKGROUND, PEAK_CONDUCTIVITY, PEAK SIZE, ARRIVAL, PEAK, FLUSH")
    print(str(round(float(background),3))+" "+str(round(float(peak_conductivity),3))+" "+str(round(peak_size,3))+" "+str(round(float(ARRIVAL),3))+" "+str(round(float(PEAK),3))+" "+str(round(float(FLUSH),3)))

#del peak_size
    
###UPEPR####
SONDE = 'Upper ms/cm'
COLUMN = 2
peak_calc()

SONDE = 'Lower ms/cm'
COLUMN = 3
peak_calc()

