# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:57:32 2023

@author: Seyi Falope
"""

# importing necessary libraries for Analysis

import matplotlib.gridspec as gs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
The Analysis of the topic of focus for this project requires different datasets, which will all be read in for analysis
"""

# Reading in dataset on military expenditure
exp = pd.read_csv('API_MS.MIL.XPND.CD_DS2_en_csv_v2_5363327.csv', skiprows=4)
print(exp.head())

# Reading in datasets on conflict death
death = pd.read_csv('deaths-in-state-based-conflicts-by-world-region.csv')
print(death.head())

# Reading in datasets on History of conflict
history = pd.read_csv('conflicts and wars - Sheet1.csv')
print(history.head())

"""
Beginning with the expenditure data, i will be exploring the data to understand and learn more about it
and perform some data wrangling exerices to make the data easy to analyze
"""

# Checking information about the data and its structure
print(exp.info())

# dropping categorical columns not needed in our analysis
exp.drop(columns=['Country Code', 'Indicator Name',
         'Indicator Code'], inplace=True)

# Checking descriptive statistics of the data
print(exp.describe())

# Checking for missing values
print(exp.isna().sum())  # there are missing values in our data

# Dealing with the missing data
print(exp.fillna(0, inplace=True))  # Filling all missing data with 0 values

"""
Since we are focusing on region wise analyis, the datset will be filtered to
include only regions as outlined by the World Bank
"""

# Filtering our data to only regions as outlined by world bank
fil = exp['Country Name'].isin(['East Asia & Pacific', 'Europe & Central Asia', 'Latin America & Caribbean',
                                'Middle East & North Africa', 'South Asia', 'Sub-Saharan Africa', 'North America'])

exp = exp[fil]  # filtering countries out from dataframe
exp.reset_index(drop=True, inplace=True)  # reseting the index


# Analyzing the trend of expenditure across the years for each region
exp_year = exp.T  # Transposing the data
exp_year.columns = exp_year.iloc[0]  # Making the first row the column name
exp_year = exp_year.iloc[1:]  # filtering only for years
# changing the datatype
exp_year = exp_year.apply(pd.to_numeric, errors='coerce')
# Calculating total expenditure for each yeqar
exp_year['Total'] = exp_year.sum(axis=1)
exp_year = exp_year.reset_index()  # reset the index
exp_year.rename(columns={'index': 'Year'}, inplace=True)  # renaming columns
exp_year['Year'] = exp_year['Year'].astype(
    'float')  # changing the year to a date
print(exp_year.head())

# calculating total expenditure for each region
exp['Total'] = exp.sum(axis=1)
exp_region = exp.sort_values('Total')  # sorting the data in descending order
print(exp_region.head())


'''
Next is the exploration and analysis of  the dataset involving conflict deaths
'''
# Checking basic information about the dataset
print(death.info())

# Checking summary statistic
print(death.describe())

# checking for missing data
print(death.isna().sum())  # No missing data

# Checking for regions in the data
print(death['Entity'].value_counts())

# renaming the column
print(death.rename(columns={
      'Deaths in all state-based conflict types': 'Total Death'}, inplace=True))


# Filtering data to only regions
filt = death['Entity'].isin(
    ['Africa', 'Americas', 'Asia & Oceania', 'Europe', 'Middle East'])

death_region = death[filt]


# Grouping the data by region
death_region = death_region.groupby('Entity')['Total Death'].sum()

death_region = pd.DataFrame(death_region)  # converting to a dataframe format

print(death_region)


'''
Lastly, i will be exploring a the data on the history of conflict to analyze  regions 
where conflict took place the most from 1960 to date
'''

history.head()

# checking info about the data and its structure
print(history.info())

# checking if there are missing values in our data
# we have no missing data in the columns we want to use for our analyzing
print(history.isna().sum())

# filtering the data from years 1960-2022
year = (history['Date'] >= '1960') & (history['Date'] <= '2022')
history = history[year]
print(history)

# checking the  regions  columns to ensure no duplicates
print(history['Region'].value_counts())

# renaming and replacing misspelt regions
history['Region'] = history['Region'].replace({'Latin America and the Ca': 'Latin America and the Caribbean',
                                              'Latin America & the Caribbean': 'Latin America and the Caribbean',
                                               '*Western Asia': 'Western Asia'})

# counting regions where conflict occurs the most
conflict_region = history['Region'].value_counts()
print(conflict_region.head())

# converting this to a Dataframe
conflict_region = pd.DataFrame(conflict_region)
conflict_region = conflict_region.reset_index()  # resetting the index
print(conflict_region.head())

# renaming the columns
conflict_region.columns = ['Region', 'Total Number']
# filtering out regions with no/insignificant occurence of war
conflict_region = conflict_region.head(10)
print(conflict_region.head)


# Creating a dash board

# Setting the style
plt.style.use('seaborn-talk')

# creating a figure
fig = plt.figure(figsize=(11, 11), dpi=300)

# creating a gridspec object
gs = gs.GridSpec(4, 4, wspace=0.8, hspace=1.3)

ax1 = plt.subplot(gs[0:2, 1:4])  # line plot
ax1.plot(exp_year['Year'], exp_year['Sub-Saharan Africa'],
         label='Sub-Saharan Africa')
ax1.plot(exp_year['Year'], exp_year['South Asia'], label='South Asia')
ax1.plot(exp_year['Year'], exp_year['North America'], label='North America')
ax1.plot(exp_year['Year'], exp_year['Middle East & North Africa'],
         label='Middle East & North Africa')
ax1.plot(exp_year['Year'], exp_year['Latin America & Caribbean'],
         label='Latin America & Caribbean')
ax1.plot(exp_year['Year'], exp_year['Europe & Central Asia'],
         label='Europe & Central Asia')
ax1.plot(exp_year['Year'], exp_year['East Asia & Pacific'],
         label='East Asia & Pacific')
ax1.legend(fontsize=8)
ax1.set_title('Trend of Region Military Expenditure (1960-2021)',
              size=14, weight=1000)
ax1.set_xlabel('Year', weight=1000, size=12)
ax1.set_ylabel('Expenditure (in Billions USD)', weight=1000, size=12)

# plotting a bar chart to show total expenditure for each region
ax2 = plt.subplot(gs[0:2, 0:1])  # pie chart
ax2.barh(exp_region['Country Name'], exp_region['Total'], color='r')
ax2.set_title('Military Expenditure by Region',
              size=13, weight=1000)
ax2.set_xlabel('Expenditure (in Billions USD)', size=12, weight=1000)
ax2.set_ylabel('Region', size=14, weight=1000)

# plotting a bar chart to visualize a number of occurrences in regions
ax3 = plt.subplot(gs[2:4, 0:2])  # bar plot
ax3.barh(conflict_region['Region'], conflict_region['Total Number'])
plt.gca().invert_yaxis()
ax3.set_title('Regions With Most Conflicts', size=14, weight=1000)
ax3.set_xlabel('Number of Conflicts', size=12, weight=1000)
ax3.set_ylabel('Region', size=12, weight=1000)

# Plotting a pie chart to show proportion of total death by region
ax4 = plt.subplot(gs[2:4, 2:4])  # pie chart
ax4.pie(death_region['Total Death'], labels=death_region.index)
ax4.set_title('Distribution of Death by Regions', size=14, weight=1000)
ax4.set_xlabel('Proportion of Total Death', size=14, weight=1000)


# create a text box with summary of the our dashboard and analysis
summary_text = "Summary Report\n\nThis project analyzed military spending and human casualties resulting from war across different regions of the world \n\nfrom 1960 to 2021.The study found that military expenditure has been increasing in all regions, with a significant spike in 2010.\n\nNorth America was identified as the highest spender on military, followed by Europe and East Asia.The Middle East & North Africa \n\nregion had the most conflicts during the period, with Asia & Oceania having the highest number of deaths, followed by Africa.\n\nAlthough regions with higher military spending tended to have fewer casualties, conflicts still resulted in significant human casualties."

textbox = plt.text(0.5, -0.1, summary_text, transform=fig.transFigure,
                   fontsize=15, fontweight='bold', horizontalalignment='center')

plt.subplots_adjust(bottom=0.2)


# Adding a subtitle to the Dashboard
plt.suptitle('Region Wise Analysis of Military Expenditure and Human Casualties(1960-2021)\n\nBy SEYI FALOPE \n\n(Student Number: 22023879)',
             weight=1000, size=19, y=1.08)
plt.subplots_adjust(top=0.9)


# Setting a boarderline around the dashboard
fig = plt.gcf()
fig.patch.set_linewidth('5')  # set the width of the figure border
fig.patch.set_edgecolor('black')  # set the color of the figure border


# Saving the dashboard as a PNG file
plt.savefig('22023879.png', dpi=300)

plt.show()
