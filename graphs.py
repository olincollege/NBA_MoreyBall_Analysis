from data_analysis import *
from scraper import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(42)
import plotly.graph_objects as go

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

    df = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(df))
    plt.show()

def interactive_map(team, title):
    """
    Generates interactive map based on team names (includes playoffs)
    """
    df = team_summary(team)
    fig = go.Figure()
    for column in df.columns.to_list():
        fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[column],
                name = column
            )
        )

    button_initial = dict(label = 'Please Select One', method = 'update',
                      args = [{'title':'Please Select One',
                               'showlegend':True}])

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'visible': df.columns.isin([column]),
                             'title': column,
                             'showlegend': True}])

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = [button_initial] + list(df.columns.map(lambda column: create_layout_button(column)))
            )
        ],
         yaxis_type="log"       
    )
    fig.update_layout(
        title_text=f"{team} Team Summary",
        height=800
    )
    fig.show()