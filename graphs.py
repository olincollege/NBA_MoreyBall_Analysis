from data_analysis import *
from scraper import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(42)
import plotly.graph_objects as go
import matplotlib


def season_summary_visual(stat, playoff, y_label, title):
    """
    Trend over time of the league average of a single stat, visualized
    as a matplotlib scatter plot.

    Args:
        stat: A string representing the stat in the header to plot (all possible
        'stats' are inside of the DATA_NAMES dictionary)
        playoff: A boolean saying whether to plot playoffs data or regular
        season.
        y_label: String representing the desired y-label of the plot.
        title: String representing the desired title of the plot.
    """

    head_list = list(DATA_NAMES.keys())
    try:
        stat_index = head_list.index(stat)
    except(ValueError):
        return "Stat does not exist in data."
    data = []
    year = []
    for i in range(10,21):
        if playoff:
            all_stats = season_summary(f'20{i}', True)
        else:
            all_stats = season_summary(f'20{i}', False)

        data.append(float(all_stats.iloc[0, stat_index]))
        year.append(f'{i-1}-{i}')

    plt.plot(year, data)
    plt.scatter(year, data)
    plt.xlabel('Season')
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def team_summary_visual(team, stat, playoff):
    """
    Trend over time of a stat for a single team, visualized as a matplotlib
    scatter plot.

    Args:
        team: A string representing the team name
        stat: String representing the desired stat to pull data for
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.
    """
    team_stats = team_summary(team)
    print(team_stats)
    stats = {}
    nums_for_stat = list(team_stats.loc[:,stat])
    print(nums_for_stat)
    for i in range(0, team_stats.shape[0]):
        print(i)
        name = team_stats.iloc[i].name
        if name[len(name)-5:len(name)-4] == 'p' and playoff:
            stats[name[2:4]] = round(float(nums_for_stat[i]),3)
        elif name[len(name)-5:len(name)-4] == 'p' and not playoff:
            continue
        elif name[len(name)-5:len(name)-4] != 'p' and not playoff:
            stats[name[2:4]] = round(float(nums_for_stat[i]),3)
        else:
            continue
    
    sorted_year = sorted(stats.items())
    sorted_stat = dict(sorted_year)
    plt.plot(list(sorted_stat.keys()), list(sorted_stat.values()))
    plt.scatter(list(sorted_stat.keys()), list(sorted_stat.values()))
    plt.xlabel('Season')
    plt.ylabel(stat)
    plt.show()


def win_compare(year,stat_nba, playoff, xlabel, ylabel, title):
    """
        Args:
            year: Int representing the year to pull data for
            stat_nba:

    """

    year = str(year)
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
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def seaborn_plots(stat_nba, playoff):

    df = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(df))
    plt.show()


def seaborn_plots_silent(stat_nba, playoff):

    df = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(df))


def efg_vs_3PA():
    efgs = get_efg()
    sns.boxplot(x="Year", y="eFG%", data=efgs)
    plt.show()


def playoff_3P_chart(year, playoffs):
    data = playoff_round_3P(year, playoffs)
    labels = list(data.keys())
    threes_attempted = []
    threes_made = []

    for i in range(0,len(data)):
        threes_attempted.append(data[i][0])
        threes_made.append(data[i][1])
    
    width = 0.35

    x = np.arange(len(labels))
    fig,ax = plt.subplots()
    rects1 = ax.bar(x - width/2, threes_attempted, width, label="% Shots Attempted from 3PT")
    rects2 = ax.bar(x + width/2, threes_made, width, label="% 3PT Shots made")

    ax.set_ylabel('Percentage (as decimal)')
    ax.set_title(f'Three Point Shooting by Playoffs Outcome ({year})')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.show()


def edge_case_graph():
    fig, ax = plt.subplots()
    data = edge_cases_metric()
    x = np.arange(len(list(data.keys())))
    ax.bar(x, list(data.values()), 0.35, label="Edge Cases")
    ax.set_xticks(x)
    ax.set_xticklabels(list(data.keys()))
    ax.set_ylabel('Number of Edge Cases')
    ax.set_xlabel('Season')
    fig.tight_layout()
    plt.show()


def playoffs_versus_season():
    """
    Plots %3PA and %3PM for regular season and playoffs
    """
    plt.subplot(221)
    seaborn_plots_silent('Field_Goals_Attempled_3PA', False)
    #season_summary_visual('Field_Goals_Attempled_3PA', False, 'Pct. of Shots Attempted from 3PT', '3PT Attempts Regular Season')
    plt.subplot(222)
    seaborn_plots_silent('Field_Goals_Attempled_3PA', True)
    plt.subplot(223)
    seaborn_plots_silent('Field_Goals_3P', False)
    plt.subplot(224)
    seaborn_plots_silent('Field_Goals_3P', True)
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



