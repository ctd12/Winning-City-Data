# %%
import pandas as pd
import os
import ast

# %%
# Importing the CSV and saving it as a Pandas DataFrame

pwd = os.getcwd()
filepath = pwd + '/case1.csv'
city_data = pd.read_csv(filepath)
del city_data['index']
city_data.rename(columns = {'key': 'City'}, inplace = True)
city_data

# Description of the CSV: This file contains championship data from 1870-2018, including teams, sports, and results.

# "key" column: city, state
# "values" column: list of dictionaries; each dictionary is a year (ascending) that a team from that city won a championship
# "seasons" column: how many seasons of each sports league have taken place in the city

# %%
# Each "values" value is a string, it needs to be a list of dictionaries

# Remove the brackets at the beginning of each string
def remove_brackets(string):
    remove_front = string.replace('[', '')
    remove_back = remove_front.replace(']', '')
    return remove_back


# %%
# Turn the string into a list, separated by dictionary brackets.

def string_to_list(string):
    new_list = []
    new_string = ''
    for i in string:
        if i == '}':
            new_string += i
            new_list.append(new_string)
            new_string = ''
        else:
            new_string += i
    return new_list


# %%
# Remove the ', ' that is at the beginning of every string after the first one in the list.

def remove_comma_space(team_list):
    new_team_list = []
    for i in team_list:
        if i[0] == '{':
            new_team_list.append(i)
        else:
            new_team = i[2:]
            new_team_list.append(new_team)
    return new_team_list


# %%
# Finally, transform each item in the list from a string into a dictionary. The dictionaries can now be manipulated.

def strings_to_dicts(list_of_strings):
    list_of_dicts = []
    for i in list_of_strings:
        result = ast.literal_eval(i)
        list_of_dicts.append(result)
    return list_of_dicts


# %%
# Replace the values column (string values) with a new values column that contains lists of dictionaries. 
# Each dictionary contains information about a team that won a championship from that city (year, team, and sport).

champions = []
values_list = city_data['values']

for value in values_list:
    rb = remove_brackets(value)
    stl = string_to_list(rb)
    rcs = remove_comma_space(stl)
    final = strings_to_dicts(rcs)
    champions.append(final)

city_data['values'] = champions
city_data['# of City Championships'] = city_data['values'].str.len()
city_data

# %%
# Plot relationship of population vs. # of championships

import matplotlib.pyplot as plt
import numpy as np

x = np.array(city_data['population'])
y = np.array(city_data['# of City Championships'])

plt.scatter(x, y)
plt.xlabel('Population', fontweight = 'bold')
plt.ylabel('Championships', fontweight = 'bold')
plt.title('Relationship between Population and Championships', fontweight = 'bold')
plt.show()

# %%
# Remove the outliers to have a better visual

x_sorted = np.sort(x)
x_high_to_low = x_sorted[::-1]
print(x_high_to_low[0:10])

# %%
x_high_one = x_high_to_low[0]
x_high_two = x_high_to_low[1]

index_one = np.where(x == x_high_one) # index 20
index_two = np.where(x == x_high_two) # index 25

x2 = np.delete(x, 25)
x2 = np.delete(x2, 20)
y2 = np.delete(y, 25)
y2 = np.delete(y2, 20)

plt.scatter(x2, y2)
plt.ticklabel_format(style = 'plain')
plt.xlabel('Population', fontweight = 'bold')
plt.ylabel('Championships', fontweight = 'bold')
plt.title('Relationship between Population and Championships', fontweight = 'bold')
plt.show()

# %%
# This shows that when removing the largest two outliers in terms of population
# there is not direct correlation between the population of a city and the total sports championships it has.
# However, cities with larger populations tend to have at least one championship.
# Most cities have close to, if not zero sports championships.

np.corrcoef(x, y)

# %%
np.corrcoef(x2, y2)

# %%

# Next is an analysis of the amount of National Hockey League champoinships each city has gotten.

nhl_champs = []
all_champs = city_data['values']

# Nested for loop to get the total number of championship seasons by sport for each city.

for champ_list in all_champs: 
    city_nhl_champs = 0
    for champ_dictionary in champ_list: 
        for key, value in champ_dictionary.items():
            if key == 'sport':
                if value == 'nhl':
                    city_nhl_champs += 1
    nhl_champs.append(city_nhl_champs)

city_data['NHL Championships'] = nhl_champs
city_data

# %%
# Creating a new data frame to analyze NHL championships per city

nhl_data = city_data[['City', '# of City Championships', 'NHL Championships']]

# New column displaying the % of NHL / Total City Championships

nhl_v2 = nhl_data.copy()
nhl_v2['NHL Percentage of Total'] = (nhl_v2['NHL Championships'] / nhl_v2['# of City Championships'] * 100).round(2)

# Creating a mask to filter out cities with 0 NHL championships

mask = nhl_v2['NHL Championships'] != 0
nhl_totals = nhl_v2[mask]

# NHL % highest to lowest

nhl_totals = nhl_totals.sort_values(by = ['NHL Percentage of Total'], ascending = False)
nhl_totals

# %%
# Creating a bar graph to display the top 10 cities in terms of the highest percentages of NHL titles out of total

cities = nhl_totals['City']
percentages = nhl_totals['NHL Percentage of Total']

plt.bar(cities[0:10], percentages[0:10], color = 'green', width = 0.5)

plt.xlabel('City', fontweight = 'bold')
plt.ylabel('NHL Championships Over Total (%)', fontweight = 'bold')
plt.title('Top 10 Hockey Cities in terms of % Total Championships', fontweight = 'bold')
plt.xticks(rotation = 80)

plt.show()