# Written by Emily Adams, Summer 2021, Kostal Research Group at The George Washington University
# Tool for data cleaning, KS/RS/Rf/RLf assignment to prepare toxicological data for MUST

import pandas as pd
import os
import glob
from must_plot import*

def toxicology_csv_to_df(some_csv):
    tox_data = pd.read_csv(some_csv, header=0, names=['Name', 'CAS', 'Species', 'Measure', 'Route', 'Value', 'Unit',
                                                      'KS', 'RS', 'Rf', 'RLf', 'Source', 'Year', 'Study', 'Link', ''], low_memory=False)
    return tox_data

#dtype={'Name': str, 'CAS': int, 'Species': str, 'Measure': int, 'Route': str, 'Value': float, 'Unit': str, 'KS': int, 'RS': int, 'Rf': int, 'RLf': float, 'Source': str, 'Year': int}
df = toxicology_csv_to_df('/home/emily/CodeLyfe/Research/MUST_original_and_perl/Curated ToxNet Data for MUST - batch_NLM.csv')
#df = toxicology_csv_to_df('/home/emily/CodeLyfe/Research/MUST_original_and_perl/must_aquatic_tox_all.csv')

df = df[df['Name'].notna()]

# If units in mg/m3 or mL/kg, convert to mg/kg by dividing or multiplying corresponding value in column 'Value' by 1000.
# Convert all other viable units to mg/kg with conversion factor of 1.

df['Unit'] = df['Unit'].replace(['ppm', 'm1484g/kg', 'mL/m3'], 'mg/kg')

for index, row in df.iterrows():
    if row['Unit'] == 'mL/kg':
        df.at[index, 'Value'] = row['Value']*1000
        df.at[index, 'Unit'] = 'mg/kg'

for index, row in df.iterrows():
    if row['Unit'] == 'mg/m3':
        df.at[index, 'Value'] = row['Value']/1000
        df.at[index, 'Unit'] = 'mg/kg'

# Species stuff: rename some species types

df['Species'] = df['Species'].replace(['8rat', 'rat8'], 'rat')
df['Species'] = df['Species'].replace(['mammal (species unspecified8)', 'mammal '], 'mammal')

# Determining sorts of species that occur in final groups using set.

#set_species = set()
#s_groups = df.groupby(['Species'])
#for group in s_groups:
#vals, df = group
#set_species.add(vals)
#print(set_species)

# Assigning KS values based on species relevance to humans

# RELIABILITY_SCORES = {
#     'mammal': 4,
#     'frog': 4,
#     'domestic animals - goat/sheep': 3,
# }
# for index, row in df.iterrows():
#     df.at[index, 'KS'] = RELIABILITY_SCORES[row['Species']]

for index, row in df.iterrows():
    if row['Species'] == 'mammal':
        df.at[index, 'RS'] = 17
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'frog':
        df.at[index, 'RS'] = 15
        df.at[index, 'RLf'] = 0.5
    if row['Species'] == 'domestic animals - goat/sheep':
        df.at[index, 'RS'] = 20
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'horse/donkey':
        df.at[index, 'RS'] = 20
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'bird - domestic':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5
    if row['Species'] == 'bird - wild':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5

for index, row in df.iterrows():

    if row['Species'] == 'quail':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5
    if row['Species'] == 'turkey':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5
    if row['Species'] == 'cattle':
        df.at[index, 'RS'] = 20
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'chicken':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5
    if row['Species'] == 'pigeon':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5
    if row['Species'] == 'duck':
        df.at[index, 'RS'] = 16
        df.at[index, 'RLf'] = 0.5

for index, row in df.iterrows():
    if row['Species'] == 'cat':
        df.at[index, 'RS'] = 20
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'guinea pig':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'pig':
        df.at[index, 'RS'] = 20
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'dog':
        df.at[index, 'RS'] = 20
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'squirrel':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'rat':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'gerbil':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'hamster':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'rabbit':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'mouse':
        df.at[index, 'RS'] = 21
        df.at[index, 'RLf'] = 0.6
    if row['Species'] == 'monkey':
        df.at[index, 'RS'] = 25
        df.at[index, 'RLf'] = 0.8

for index, row in df.iterrows():
    if row['Species'] == 'human':
        df.at[index, 'RS'] = 30
        df.at[index, 'RLf'] = 1
    if row['Species'] == 'women':
        df.at[index, 'RS'] = 30
        df.at[index, 'RLf'] = 1
    if row['Species'] == 'man':
        df.at[index, 'RS'] = 30
        df.at[index, 'RLf'] = 1
    if row['Species'] == 'child':
        df.at[index, 'RS'] = 30
        df.at[index, 'RLf'] = 1
    if row['Species'] == 'infant':
        df.at[index, 'RS'] = 30
        df.at[index, 'RLf'] = 1

# KS to Rf
for index, row in df.iterrows():
    if row['KS'] == 1:
        df.at[index, 'Rf'] = 1
    if row['KS'] == 2:
        df.at[index, 'Rf'] = 0.7
    if row['KS'] == 3:
        df.at[index, 'Rf'] = 0.3
    if row['KS'] == 4:
        df.at[index, 'Rf'] = 0.1

# Group by CAS ID number and measurement type.
# Remove rows for chemicals with less than 10 measurement values with the same measurement type and units.
# Save as smaller csv files grouped by CAS number and measurement type in folders based on number of threshold measurements
# (10 - 100).

files = glob.glob('cleaned_csv_output/*.csv')
for f in files:
    os.remove(f)

groups = df.groupby(['Name', 'Measure', 'Route'])
for group in groups:
    vals, df = group
    #df = df.rename(columns={'Source': 'X'})
    #df = df.assign(X='X')
    df = df[['Name', 'CAS', 'Species', 'Measure', 'Route', 'Value', 'Unit', 'KS', 'RS', 'Rf', 'RLf', 'Source', 'Year']]
    df = df.drop_duplicates(subset=['Name', 'CAS', 'Species', 'Measure', 'Route', 'Value'])
    if df.shape[0] >= 10:
        df.to_csv('cleaned_csv_output/{}_{}_{}_{}.csv'.format(vals[0], vals[1], vals[2], df.shape[0]),
                  header=False, index=False)

gen_stats_and_histo_plot(files)
