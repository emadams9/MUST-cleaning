# Written by Emily Adams, Summer 2021, Kostal Research Group at The George Washington University
# Data plotting tool for MUST

import matplotlib as mpl
import pandas as pd
import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plot


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
        g_mean = stats.gmean(tox_df['Value'])
        mci = mean_confidence_interval(tox_df['Value'], confidence=0.95)
        g_mci = gmean_confidence_interval(tox_df['Value'], confidence=0.95)

        x = np.array(tox_df['Value'])

        fig, axs = plot.subplots(1, 2, figsize=(15, 6), tight_layout=True)
        axs[0].axis('tight')
        axs[0].axis('off')
        cell_text = [[min_val], [max_val], [mean], [median], [std], [g_mean], [mci], [g_mci]]
        row_labels = ('Minimum Value', 'Maximum Value', 'Mean', 'Median', 'Standard Deviation', 'Geometric Mean',
                      '95% Confidence Interval (M, –EBM, +EBM)', '95% Confidence Interval (GM, –EBGM, +EBGM)')
        axs[0].table(cellText=cell_text, rowLabels=row_labels, colLabels=None, colWidths=[1, 1], loc='center',
                     fontsize=25)
        axs[1].hist(x, bins=5)
        axs[1].axis([0, x.max() + 1, 0, len(x)])
        axs[1].set_ylabel('Frequency')
        axs[1].set_xlabel('Threshold Values')
        axs[1].set_title('Plot for File: ' + str(f))
        fig.savefig('cleaned_csv_output/{}_plot_and_stats.png'.format(tox_df['CAS'][0]))
        plot.close(fig)

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
