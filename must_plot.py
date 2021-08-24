# Written by Emily Adams, Summer 2021, Kostal Research Group at The George Washington University
# Data plotting tool for MUST


import pandas as pd
import os
import glob
import numpy as np
from scipy import stats
import matplotlib.pyplot as plot


files = glob.glob('cleaned_csv_output/*.csv')


# Takes MUST data csv files (that were sorted and cleaned by main.py) as input
# Calculates mean, median, standard dev, geometric mean, confidence interval (using mean and geometric mean)
# Rounds to 3 decimal places
# Function for plotting histograms with csv data
# Calculations and histograms are then saved to same png file

def gen_stats_and_histo_plot(must_data_csvs):
    png = glob.glob('plots_and_stats_output/*.png')
    for p in png:
        os.remove(p)

    for f in must_data_csvs:
        decimal_places = 3
        tox_df = pd.read_csv(f, names=['Name', 'CAS', 'Species', 'Measure', 'Route', 'Value', 'Unit', 'KS', 'RS', 'Rf', 'RLf',
                                       'Source', 'Year'])
        min_val = tox_df['Value'].min().round(decimal_places)
        max_val = tox_df['Value'].max().round(decimal_places)
        mean = tox_df['Value'].mean().round(decimal_places)
        median = tox_df['Value'].median().round(decimal_places)
        std = tox_df['Value'].std().round(decimal_places)
        g_mean = stats.gmean(tox_df['Value']).round(decimal_places)
        mci = [val.round(decimal_places) for val in mean_confidence_interval(tox_df['Value'], confidence=0.95)]
        g_mci = [val.round(decimal_places) for val in gmean_confidence_interval(tox_df['Value'], confidence=0.95)]

        x = np.array(tox_df['Value'])

        fig, axs = plot.subplots(1, 2, figsize=(15, 6), tight_layout=True)
        axs[0].axis('tight')
        axs[0].axis('off')
        axs[0].set_title('Statistical Analysis for File')
        cell_text = [['Statistical Analysis Values (' + (tox_df['Unit'][0]) + ')'], [tox_df.shape[0]],
                     [tox_df['Measure'][0]], [min_val], [max_val], [mean],
                     [median], [std], [g_mean], [mci], [g_mci]]
        row_labels = ('Value/Calculation', 'Number of Threshold Measurements', 'Threshold Measurement Type',
                      'Minimum Value', 'Maximum Value', 'Mean', 'Median', 'Standard Deviation',
                      'Geometric Mean', '95% Confidence Interval (M, –EBM, +EBM)',
                      '95% Confidence Interval (GM, –EBGM, +EBGM)')
        axs[0].table(cellText=cell_text, rowLabels=row_labels, colLabels=None, colWidths=[1, 1], loc='center',
                     fontsize=20)
        axs[1].hist(x, edgecolor='k', bins=5)
        axs[1].axis([0, x.max() + 1, 0, len(x)])
        axs[1].set_ylabel('Frequency')
        axs[1].set_xlabel('Category of Concern ' + ' (' + tox_df['Unit'][0] + ')')
        axs[1].set_title('Plot for File: ' + str(f))
        fig.savefig('plots_and_stats_output/{}_{}_plot_and_stats.png'.format(tox_df['Name'][0], tox_df['Measure'][0],
                                                                             tox_df['Route'][0]))
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
