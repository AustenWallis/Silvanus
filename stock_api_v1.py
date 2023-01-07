# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 23:53:10 2022

@author: riggs
"""
# --------------------------------
# IMPORTS
# --------------------------------
# ~pip install pycodestyle #python pep8 code checker~

import csv
import requests
import matplotlib.pyplot as plt
import numpy as np
import math as m
import datetime as dt
import matplotlib.dates as mdates

# --------------------------------
# API DOCUMENTATION
# --------------------------------

# https://www.alphavantage.co/documentation/

# --------------------------------
# USER INTERFACE
# --------------------------------

function = "TIME_SERIES_INTRADAY"
# ALL POSSIBLE FUNCTIONS ---
# TIME_SERIES_INTRADAY_EXTENDED #use csv
# TIME_SERIES_DAILY
# TIME_SERIES_WEEKLY
# TIME_SERIES_WEEKLY_ADJUSTED
# TIME_SERIES_MONTHLY
# TIME_SERIES_MONTHLY_ADJUSTED

ticker = "TSLA"

interval = "15min"
# ALL POSSIBLE INTERVALS ---
# 1min,5min,15min,30min,60min

size = 'compact'
# ALL POSSIBLE SIZES ---
"""compact, full"""

# --------------------------------
# STOCK MARKET API
# --------------------------------

# API dictionary ~open, high, low, close prices and volume~
# Fixed call code, DON'T FIDDLE!

# ~CSV for reduced memory with extended data~
if function == "TIME_SERIES_INTRADAY_EXTENDED":

    CSV_URL = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval={interval}&slice=year2month12&apikey=UI411LQPQUVAIF0V"
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data = list(cr)
        for row in data:
            print(row)
else:
    url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval={interval}&outputsize={size}&apikey=UI411LQPQUVAIF0V"
    r = requests.get(url)
    data = r.json()


# --------------------------------
# CANDLESTICK GRAPHING
# --------------------------------

# EXTENDED TRADING INCLUDED 4AM to 8PM US EASTERN
    # ADD OUT OF HOURS SHADING ON THE GRAPH
    # AT CORRECT TIMINGS ON THE X AXIS AND FIX PLOTTING

# Setting up datasets empty lists
time = []
Open = []
Close = []
High = []
Low = []
Volume = []

# String of date/time from the data
datasorted = sorted(data[f'Time Series ({interval})'])
# Listing api dictionary data in the time units order
for i in datasorted:
    time.append(i)
    Open.append(float(data[f'Time Series ({interval})'][i]['1. open']))
    Close.append(float(data[f'Time Series ({interval})'][i]['4. close']))
    High.append(float(data[f'Time Series ({interval})'][i]['2. high']))
    Low.append(float(data[f'Time Series ({interval})'][i]['3. low']))
    Volume.append(float(data[f'Time Series ({interval})'][i]['5. volume']))

# Setting empty lists for candle plots
height = []     # Height of the candle, open close difference.
bottom = []     # Lowest point of the candle.
colours = []    # Candle colour.
hlmid = []      # High low stick list.
hlerror = []    # Symmetric error lenght.

# Loop across all time data points.
for i in range(len(time)):

    # Green Candle
    if Close[i] > Open[i]:
        bottom.append(Open[i])              # Lowest point of the candle.
        height.append((Close[i]-Open[i]))   # Height of the candle.
        colours.append('green')             # Candle colour.
        err = (High[i]-Low[i])/2            # Symmetric high/low wick error.
        hlmid.append((Low[i]+err))          # Midpoint of the wick.
        hlerror.append(err)                 # Plot high/low wick error.

    # Red Candle, See green candle comments.
    if Open[i] > Close[i]:
        bottom.append(Close[i])
        height.append((Open[i]-Close[i]))
        colours.append('red')
        err = (High[i]-Low[i])/2
        hlmid.append((Low[i]+err))
        hlerror.append(err)

    # Black Candle, See green candle comments.
    elif Close[i] == Open[i]:
        bottom.append(Close[i])
        height.append((Open[i]-Close[i]))
        colours.append('black')
        err = (High[i]-Low[i])/2
        hlmid.append((Low[i]+err))
        hlerror.append(err)


# Converting the string of 'date/time' into datetime.
xtimedata = [dt.datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in time]
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M %d-%b'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))

plt.rcParams['figure.dpi'] = 300            # Higher resolution plot.
# Time, height, bottom.
plt.bar(xtimedata, height, width=0.01, bottom=bottom, color=colours)
for i in range(len(time)):
    plt.errorbar(xtimedata[i], hlmid[i], yerr=hlerror[i], color=colours[i],
                 elinewidth=0.3)

plt.xlabel('Time')          # Editing plot display.
plt.ylabel('Price ($)')
plt.xticks(rotation=45, ha='center')
plt.title(f'${ticker}')
plt.show()

t = np.arange(len(time)).tolist()
plt.bar(t, height, width=0.01, bottom=bottom, color=colours)
for i in range(len(time)):
    plt.errorbar(t[i], hlmid[i], yerr=hlerror[i], color=colours[i],
                 elinewidth=0.3)

plt.show()

#Adding an extra line













































