# Written by Emily Adams, Summer 2021, Kostal Research Group at The George Washington University
# Data plotting tool for MUST

import matplotlib as mpl
import pandas as pd
import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


files = glob.glob('cleaned_csv_output/*.csv')
#gen_stats_calculator(files)

# Takes MUST data csv files (that were sorted and cleaned by main.py) as input.
# Calculate mean, median, standard dev, geometric mean, confidence interval (using mean and geometric mean)
# Add to csv with histogram and export

def gen_stats_calculator(must_data_csvs):
    for f in must_data_csvs:
        tox_df = pd.read_csv(f, header=0, names=['CAS', 'Species', 'Measure', 'Value', 'Unit', 'RS', 'Source'])
        t = tox_df['Value'].min()
        u = tox_df['Value'].max()
        v = tox_df['Value'].mean()
        w = tox_df['Value'].median()
        x = tox_df['Value'].std()
        y = stats.gmean(tox_df['Value'])
        z = mean_confidence_interval(tox_df['Value'], confidence=0.95)
        zz = gmean_confidence_interval(tox_df['Value'], confidence=0.95)
        print('Minimum = ' + str(t))
        print('Maximum = ' + str(u))
        print('Mean = ' + str(v))
        print('Median = ' + str(w))
        print('Standard Deviation = ' + str(x))
        print('Geometric Mean = ' + str(y))
        print('95% Confidence Interval (M, –EBM, +EBM) = ' + str(z))
        print('95% Confidence Interval (GM, –EBGM, +EBGM) = ' + str(zz))

# Functions for calculating 95% CI using the mean and geometric mean

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def gmean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = stats.gmean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def histogram_plot(must_data_csvs):
    for f in must_data_csvs:
        tox_df = pd.read_csv(f, header=0, names=['CAS', 'Species', 'Measure', 'Value', 'Unit', 'RS', 'Source'])
        plt.hist(np.array(tox_df['Value']), density=True, bins=30)
        plt.ylabel('Frequency')
        plt.xlabel('Threshold Values')
        plt.show()
        break

histogram_plot(files)
