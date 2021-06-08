import pandas as pd


def toxicology_csv_to_list(some_csv):
    tox_data = pd.read_csv(some_csv, header=0, names=['', 'CAS', 'Species', 'Measure', 'Value', 'Unit', 'KS', 'Source'])
    return tox_data


df = toxicology_csv_to_list('/home/emily/CodeLyfe/Research/MUST/batch_NLM.csv')

# Regroup acute toxicity measurements

df = df.replace(['LC50', 'LCt50'], 'LD50')
df = df.replace(['TDLo', 'LCLo'], 'LDLo')
df = df.replace(['LC90'], 'LD90')
df = df.replace(['LC30'], 'LD30')

# If units in mg/m3 or mL/kg, convert to mg/kg by dividing or multiplying corresponding value in column 'Value' by 1000.
# Convert all other viable units to mg/kg with conversion factor of 1.

df = df.replace(['ppm', 'mL/m3'], 'mg/kg')

for index, row in df.iterrows():
    if row['Unit'] == 'mL/kg':
        df.at[index, 'Value'] = row['Value']*1000      # Multiple by 1000
        df.at[index, 'Unit'] = 'mg/kg'

for index, row in df.iterrows():
    if row['Unit'] == 'mg/m3':
        df.at[index, 'Value'] = row['Value'] / 1000     # Divide by 1000
        df.at[index, 'Unit'] = 'mg/kg'

# Species stuff
print(pd.value_counts('Species'))

# Assigning KS values

# Group by CAS ID number and measurement type.
# Remove rows for chemicals with less than 10 measurement values with the same measurement type and units.
# Save as smaller csv files grouped by CAS and measurement type.

groups = df.groupby(['CAS', 'Measure'])
for group in groups:
   vals, df = group
   if df.shape[0] >= 10:
        df.to_csv('CAS_{}_{}.csv'.format(vals[0], vals[1]))
