# Written by Emily Adams, Summer 2021, Kostal Research Group at The George Washington University
# Data cleaning tool to prepare csv data for MUST

import pandas as pd
import os
import glob


def toxicology_csv_to_df(some_csv):
    tox_data = pd.read_csv(some_csv, header=0, names=['', 'CAS', 'Species', 'Measure', 'Value', 'Unit', 'RS', 'Source'])
    return tox_data


df = toxicology_csv_to_df('/home/emily/CodeLyfe/Research/MUST_original_and_perl/batch_NLM.csv')

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
    if row['Species'] == 'frog':
        df.at[index, 'RS'] = 15
    if row['Species'] == 'domestic animals - goat/sheep':
        df.at[index, 'RS'] = 20
    if row['Species'] == 'horse/donkey':
        df.at[index, 'RS'] = 20
    if row['Species'] == 'bird - domestic':
        df.at[index, 'RS'] = 16
    if row['Species'] == 'bird - wild':
        df.at[index, 'RS'] = 16

for index, row in df.iterrows():

    if row['Species'] == 'quail':
        df.at[index, 'RS'] = 16
    if row['Species'] == 'turkey':
        df.at[index, 'RS'] = 16
    if row['Species'] == 'cattle':
        df.at[index, 'RS'] = 20
    if row['Species'] == 'chicken':
        df.at[index, 'RS'] = 16
    if row['Species'] == 'pigeon':
        df.at[index, 'RS'] = 16
    if row['Species'] == 'duck':
        df.at[index, 'RS'] = 16

for index, row in df.iterrows():
    if row['Species'] == 'cat':
        df.at[index, 'RS'] = 20
    if row['Species'] == 'guinea pig':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'pig':
        df.at[index, 'RS'] = 20
    if row['Species'] == 'dog':
        df.at[index, 'RS'] = 20
    if row['Species'] == 'squirrel':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'rat':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'gerbil':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'hamster':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'rabbit':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'mouse':
        df.at[index, 'RS'] = 21
    if row['Species'] == 'monkey':
        df.at[index, 'RS'] = 25

for index, row in df.iterrows():
    if row['Species'] == 'human':
        df.at[index, 'RS'] = 30
    if row['Species'] == 'women':
        df.at[index, 'RS'] = 30
    if row['Species'] == 'man':
        df.at[index, 'RS'] = 30
    if row['Species'] == 'child':
        df.at[index, 'RS'] = 30
    if row['Species'] == 'infant':
        df.at[index, 'RS'] = 30

# Group by CAS ID number and measurement type.
# Remove rows for chemicals with less than 10 measurement values with the same measurement type and units.
# Save as smaller csv files grouped by CAS number and measurement type in folders based on number of threshold measurements
# (10 - 100).

files = glob.glob('cleaned_csv_output/*.csv')
for f in files:
    os.remove(f)

groups = df.groupby(['CAS', 'Measure'])
for group in groups:
    vals, df = group
    #df = df.rename(columns={'Source': 'X'})
    #df = df.assign(X='X')
    df = df[['CAS', 'Species', 'Measure', 'Value', 'Unit', 'RS', 'Source']]
    df = df.drop_duplicates(subset=['CAS', 'Species', 'Measure', 'Value', 'Unit'])
    if df.shape[0] >= 20:
        df.to_csv('cleaned_csv_output/{}_{}_{}.csv'.format(vals[0], vals[1], df.shape[0]),
                  header=False, index=False)

