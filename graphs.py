from data_analysis import *
from scraper import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(42)

YEARS_LIST = ['2010','2011','2012','2013','2014', \
    '2015','2016','2017','2018','2019','2020', ]

def box_plot(stat_nba, playoff):
    """
    Box and Whisker plot for all seasons
    """
    df = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        season_full =  season_full_data(years, playoff)
        df[years] = pd.to_numeric(season_full[stat_nba])

    return df

def win_compare():

    df = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        win_data = list(get_win_data(int(years)).iloc[:,0])
        df[years] = win_data

    df.index = get_win_data(int(2010)).index
    return df

def seaborn_plots(stat_nba, playoff, x_title, y_title, label):

    df = box_plot(stat_nba, playoff)
    sns.boxplot(x=x_title, y=y_title, data=pd.melt(df))
    plt.show()


