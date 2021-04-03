from data_analysis import *
from scraper import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(42)

YEARS_LIST = ['2010','2011','2012','2013','2014', \
    '2015','2016','2017','2018','2019','2020', ]

def nba_stat_summary(stat_nba, playoff):
    """
    Gives the nba state summary
    """
    df = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        season_full =  season_full_data(years, playoff)
        df[years] = pd.to_numeric(season_full[stat_nba])

    return df

def win_compare(year,stat_nba, playoff):

    df = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        win_data = list(get_win_data(int(years)).iloc[:,0])
        games_played = int(season_summary(years, playoff).iloc[:,2])
        df[years] = [int(i) for i in win_data]
        df[years] = df[years].div(games_played).round(2)

    df.index = get_win_data(int(2010)).index
    nba_stat = nba_stat_summary(stat_nba, playoff)
    nba_stat.index = get_win_data(int(2010)).index
    plt.scatter(df[year], nba_stat[year])

def seaborn_plots(stat_nba, playoff):

    df = box_plot(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(df))
    plt.show()


