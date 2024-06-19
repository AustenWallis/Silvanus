# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 23:53:10 2022

@author: riggs
"""
# %% 
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
import config

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

ticker = "SPY"

interval = "15min"
# ALL POSSIBLE INTERVALS ---
# 1min,5min,15min,30min,60min

size = 'full'
# ALL POSSIBLE SIZES ---
"""compact, full"""

api_key = config.old_api_key
# --------------------------------
# STOCK MARKET API
# --------------------------------

# API dictionary ~open, high, low, close prices and volume~
# Fixed call code, DON'T FIDDLE!

# ~CSV for reduced memory with extended data~
if function == "TIME_SERIES_INTRADAY_EXTENDED":

    CSV_URL = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval={interval}&slice=year2month12&apikey={api_key}"
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data = list(cr)
        for row in data:
            print(row)
else:
    url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval={interval}&outputsize={size}&apikey={api_key}"
    r = requests.get(url)
    data = r.json()

# %% 
# --------------------------------
# MANUAL CANDLESTICK GRAPHING
# --------------------------------

# EXTENDED TRADING INCLUDED 4AM to 8PM US EASTERN
    # CUSTOM TIME RANGES - i want this date, range(x-y) etc
    # Plot background grid (maybe minor ticks?)
    
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

data_array = [Open, Close, High, Low, Volume]
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
    elif Open[i] > Close[i]:
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

xtimedata = [dt.datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in time] # Time data entries
x_axis = range(len(xtimedata)) # Plot's x axis to remove time gaps
today_plot_indexes = []
plot_last_day = 1 # switch to only take last day's data if desired or full range if 0
if plot_last_day == 1:
    temp_date = xtimedata[-1].date()
    for i in x_axis:
        if xtimedata[i].date() == temp_date:  # Filtering data to only contains final day
            today_plot_indexes.append(i) # Gathering the indexes
    x_axis = [x_axis[i] for i in today_plot_indexes] # Filtering to only required indexes
    bottom = [bottom[i] for i in today_plot_indexes]
    height = [height[i] for i in today_plot_indexes]
    colours = [colours[i] for i in today_plot_indexes]
    hlmid = [hlmid[i] for i in today_plot_indexes]
    hlerror = [hlerror[i] for i in today_plot_indexes]
    x_tick_labels = [xtimedata[i].time() for i in today_plot_indexes]
    x_tick_labels = x_tick_labels[0::int(len(x_axis)/20)] # Reducing the number of ticks plotted, labels for later
else:
    x_tick_labels = xtimedata[0::int(len(x_axis)/20)]     # Full data set plot labelling if switch 0

# Plotting grey shaded area when in extended hours, plt.fillbetween -10 and 1e6
lower_grey_line = [-10]*len(x_axis)
upper_grey_line = [-10]*len(x_axis)
counter = 0
for i in x_axis:
    if dt.time(4,00) <= xtimedata[i].time() < dt.time(9,30): # 4:00 am to 9:30am
        upper_grey_line[counter] = 1e6
    elif 16 <= xtimedata[i].hour <= 20: # 4:00 pm to 8:00 pm
        upper_grey_line[counter] = 1e6
    counter += 1

x_tick_location = x_axis[0::int(len(x_axis)/20)] # Reducing the number of ticks plotted, labels for later

# Time, height, bottom. Plotting the data
plt.bar(x_axis, height, width=1, bottom=bottom, color=colours) 
for i in range(len(x_axis)):
    plt.errorbar(x_axis[i], hlmid[i], yerr=hlerror[i], color=colours[i], elinewidth=1)
plt.fill_between(x_axis, lower_grey_line, upper_grey_line, alpha=0.2, color='grey')
# Editing plot display.
plt.xlabel('Time')
plt.ylabel('Price ($)')
ylimits = ((min(bottom) - ((max(bottom)-min(bottom))*0.2)), (max(bottom) + ((max(bottom)-min(bottom))*0.2)))
plt.ylim(ylimits)       # Setting the plot range to show the candlesticks
plt.xticks(ticks=x_tick_location, labels=x_tick_labels,  rotation=90, ha='center')
if plot_last_day == 1:  # Adding date at top if only last day
    plt.title(f'${ticker}: {date}')
else:
    plt.title(f'${ticker}')
plt.rcParams['figure.dpi'] = 100 # Higher resolution plot.
plt.show()

print("Finished")

#Adding an extra line

# %%
