#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:46:25 2019

@author: William Keilsohn
"""

# Import Packages:

import numpy as np
import pandas as pd
from tabulate import tabulate
from operator import itemgetter



# Load in the Data:
path = '/home/william/Documents/Class_Scripts/examples/'
file_name = path + 'Data_TripAdvisor_v1.xls'

cols = ['ID_USER', 'USER_STATE', 'USER_TIMEZONE', 'ID_HOTEL', 'HOTEL_CITY', 'HOTEL_STATE', 'HOTEL_TIMEZONE', 'TRIP_TYPE', 'RATING']

hotel_data = pd.read_excel(file_name, columns = cols) # From Ppt.
hotel_data.columns = cols

### Answer questions:

# Group the frame by hotel:
## https://stackoverflow.com/questions/18554920/pandas-aggregate-count-distinct
### Works on the bases that each hotel can only occupy one location at once...
hotels = hotel_data.groupby(['ID_HOTEL']).agg({'RATING': np.average, "ID_USER": pd.Series.nunique,"HOTEL_TIMEZONE": np.unique, "HOTEL_STATE": np.unique, "HOTEL_CITY": np.unique})
users = hotel_data.groupby('ID_USER').agg({'USER_STATE': np.unique, "USER_TIMEZONE": np.unique, "RATING": np.average})

# Question 1:
print('How many hotels were rated?', '\n','A total of ', str(len(hotels)), ' hotels were rated.', end = '\n')

# Question 2:
print('What is the average rating for each hotel?', end = '\n')
'''
Note: This is the only output that will not all be visable even with scrolling.
'''
for i in range(5, 1891, 5): # https://pypi.org/project/tabulate/
    temp_frame = hotels.iloc[(i-5):i, 0].to_frame() # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_frame.html
    print(tabulate(temp_frame, headers = 'keys', tablefmt = 'psql'))
print('\nThe overall average across hotels is ', str(round(hotels.mean().loc['RATING'], ndigits = 3)), end = '\n')

# Question 3:
print('What is the highest rated hotel in each timezone?\n ')
zones = {}
for i in hotels["HOTEL_TIMEZONE"].unique():
    zones[i] = hotels[hotels.HOTEL_TIMEZONE == i]

for key, value in zones.items(): # https://pypi.org/project/tabulate/
    print(tabulate(value[value.RATING == value['RATING'].max()], headers = 'keys', tablefmt = 'psql'), end = '\n')


# Question 4:
print('What is the highest rated hotel in Portland, OR? \n')
portland_data = hotels[hotels.HOTEL_CITY == "Portland"]
portland_data = portland_data[portland_data.RATING == portland_data['RATING'].max()]
print(tabulate(portland_data, headers = 'keys', tablefmt = 'psql'), end = '\n') # https://pypi.org/project/tabulate/


# Question 5:
print('Which state provided the most users? \n')
states = {}
for i in users["USER_STATE"].unique():
    states[i] = users[users.USER_STATE == i]

state_counts = {}    
for key, value in states.items():
    state_counts[key] = len(value)
# https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
print('The state with the most users is ', max(state_counts.items(), key = itemgetter(1))[0], '. It has a total user base of ',
      str(max(state_counts.items(), key = itemgetter(1))[1]), end = '\n')

# Question 6:
print('What time zone had the highest average hotel rating? \n')
for key, value in zones.items():
   zones[key] = value['RATING'].mean()
# https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
print('The ', max(zones.items(), key = itemgetter(1))[0], ' timezone has the greatest hotel rating with an average of ',
      str(round(max(zones.items(), key = itemgetter(1))[1], ndigits = 3)), end = '\n')

# Question 7:
print("Which state had the 'nicest' (highest rating) users? Which state had the meanest (lowest rating)? \n")
for key, value in states.items():
    states[key] = value['RATING'].mean()
# https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
print('The state with the highest rating useres is ', max(states.items(), key = itemgetter(1))[0], ' who on average rated ',
      str(round(max(states.items(), key = itemgetter(1))[1], ndigits = 3)), '.', end = '\n')
print('The state with the lowest rating useres is ', min(states.items(), key = itemgetter(1))[0], ' who on average rated ',
      str(round(min(states.items(), key = itemgetter(1))[1], ndigits = 3)), '.', end = '\n')