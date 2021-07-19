# Written by Emily Adams, Summer 2021, Kostal Research Group at The George Washington University
# Data plotting tool for MUST

import matplotlib as mpl
import pandas as pd
import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plot
from PIL import Image
import PIL


files = glob.glob('cleaned_csv_output/*.csv')


# Takes MUST data csv files (that were sorted and cleaned by main.py) as input.
# Calculate mean, median, standard dev, geometric mean, confidence interval (using mean and geometric mean)
# Function for plotting histograms with csv data
# axis([xmin,xmax,ymin,ymax])
# Add to csv with histogram and export

def gen_stats_and_histo_plot(must_data_csvs):
    for f in must_data_csvs:
        tox_df = pd.read_csv(f, names=['CAS', 'Species', 'Measure', 'Value', 'Unit', 'RS', 'Source'])
        min_val = tox_df['Value'].min()
        max_val = tox_df['Value'].max()
        mean = tox_df['Value'].mean()
        median = tox_df['Value'].median()
        std = tox_df['Value'].std()
        gmean = stats.gmean(tox_df['Value'])
        mci = mean_confidence_interval(tox_df['Value'], confidence=0.95)
        gmci = gmean_confidence_interval(tox_df['Value'], confidence=0.95)

        x = np.array(tox_df['Value'])

        table_ax = plot.subplot(121)
        table_ax.text(1, 1, 'foo')
        plot_ax = plot.subplot(122)

        plot_ax.hist(x, density=False, bins=5)
        # plot_ax.axis([0, x.max() + 1, 0, len(x)])
        # plot_ax.ylabel('Frequency')
        # plot_ax.xlabel('Threshold Values')
        # plot_ax.title('Plot for File: ' + str(f))

        plot.show()
        print('Minimum = ' + str(min_val))
        print('Maximum = ' + str(max_val))
        print('Mean = ' + str(mean))
        print('Median = ' + str(median))
        print('Standard Deviation = ' + str(std))
        print('Geometric Mean = ' + str(gmean))
        print('95% Confidence Interval (M, –EBM, +EBM) = ' + str(mci))
        print('95% Confidence Interval (GM, –EBGM, +EBGM) = ' + str(gmci))
        break

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

gen_stats_and_histo_plot(files)
