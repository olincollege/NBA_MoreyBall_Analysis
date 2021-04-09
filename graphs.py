"""
Functions to plot graphs of the analysed data.
"""
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scraper import get_win_data, get_efg
from data_analysis import season_summary, nba_stat_summary,\
    team_summary, edge_cases_metric, playoff_round_3p, DATA_NAMES, YEARS_LIST, \
        win_compare_r_squared


def season_summary_visual(stat, playoff, y_label, title):
    """
    Trend over time of the league average of a single stat, visualized
    as a matplotlib scatter plot.

    Args:
        stat: A string representing the stat in the header to plot (all possible
        'stats' are inside of the DATA_NAMES dictionary).
        playoff: A boolean saying whether to plot playoffs data or regular
        season.
        y_label: A string representing the desired y-label of the plot.
        title: A string representing the desired title of the plot.

    Returns:
        Plots a scatter of season summary of a NBA stat.
    """
    data = []
    year = []
    head_list = list(DATA_NAMES.keys())
    stat_index = head_list.index(stat)
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
    Trend over time of a stat for a single team visualized as a matplotlib
    scatter plot.

    Args:
        team: A string representing the team name.
        stat: A string representing the desired stat to pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.

    Returns:
        Plots a scatter of a single team for a single stat.
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


def win_compare(year,stat_nba, playoff, xlabel, ylabel,):
    """
    Compares the win/loss record to a NBA stat for all teams
    over one season.

    Args:
        year: An int representing the year to pull data for.
        stat_nba: A string representing the desired stat to
        pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.
        xlabel: A string label for the x-axis.
        ylabel: A string label for the y-axis.
        title: A string for the title of the plot.

    Returns:
        Plots a scatter of the win/loss record against a NBA stat
        for all teams.
    """

    year = str(year)
    win_loss_record = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        win_data = pd.read_csv(f'Data/win-loss/all_records_{year}.csv').iloc[:,1]
        games_played = int(season_summary(years, playoff).iloc[:,2])
        win_loss_record[years] = [int(i) for i in win_data]
        win_loss_record[years] = win_loss_record[years].div(games_played).round(2)

    win_loss_record.index = pd.read_csv(f'Data/win-loss/all_records_{year}.csv').index
    nba_stat = nba_stat_summary(stat_nba, playoff)
    nba_stat.index = pd.read_csv(f'Data/win-loss/all_records_{2010}.csv').index
    plt.scatter(win_loss_record[year], nba_stat[year])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"{xlabel} vs {ylabel}")
    plt.show()


def nba_stat_plot(stat_nba, playoff):
    """
    Generates a box and whisker plot of a NBA stat over
    the scrapped data frame.

    Args:
        stat_nba: A string representing the desired stat to pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.

    Returns:
        A box and whisker plot for the particular NBA stat.
    """
    stat_summary = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(stat_summary))
    plt.show()


def seaborn_plots_silent(stat_nba, playoff):
    """
    Generates a box and whisker plot of a NBA state over
    the scrapped data frame for subplots.

    Args:
        stat_nba: A string representing the desired stat to pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.

    Returns:
        A box and whisker plot for the particular NBA stat
        to be used in subplots.
    """
    stat_summary = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(stat_summary))


def efg_vs_3pa():
    """
    Creates a plot comparing the effective field goal values
    to the 3 point attempted values.

    Args:
        None.

    Returns:
        A boxplot comparing the effective field goal values
        with the 3 point attempted values.
    """
    efgs = pd.read_csv('Data/efg/efg.csv')
    sns.boxplot(x="Year", y="eFG%", data=efgs)
    plt.show()


def playoff_3p_chart(year, playoffs):
    """
    Generates a side-by-side bar chart to compare % Shots
    attempted and made for 3 pointers.

    Args:
        year: An int representing the year to pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.

    Returns:
        A side-by-side boxplot of comparing % Shots
        attempted and made for 3 pointers.
    """
    data = playoff_round_3p(year, playoffs)
    labels = list(data.keys())
    threes_attempted = []
    threes_made = []

    for i, _ in enumerate(data):
        threes_attempted.append(data[i][0])
        threes_made.append(data[i][1])

    width = 0.35

    axis_ordered = np.arange(len(labels))
    fig,sub_plots = plt.subplots()
    sub_plots.bar(axis_ordered - width/2, threes_attempted, \
        width, label="% Shots Attempted from 3PT")
    sub_plots.bar(axis_ordered + width/2, threes_made, \
        width, label="% 3PT Shots made")

    sub_plots.set_ylabel('Percentage (as decimal)')
    sub_plots.set_title(f'Three Point Shooting by Playoffs Outcome ({year})')
    sub_plots.set_xticks(axis_ordered)
    sub_plots.set_xticklabels(labels)
    sub_plots.legend()
    fig.tight_layout()
    plt.show()


def edge_case_graph(stat):
    """
    Generates bar graph to compare the edge case metric over
    the scrapped data frame.

    Args:
        None.

    Returns:
        A bar graph comparing the edge case metric.

    1 Point is added to the "edge" metric during a season if a team that is
    Top 5 in 3PA makes the playoffs.
    1 point is subtracted if a team that is Bottom 5 in 3PA makes the playoffs.
    """
    width = 0.35
    data = edge_cases_metric(stat)
    fig, sub_plots = plt.subplots()
    axis_ordered = np.arange(len(list(data['Season'])))
    
    sub_plots.bar(axis_ordered - width/2, list(data['Edge Case Metric']), \
        width, label="Edge Case Metric")
    sub_plots.bar(axis_ordered + width/2, list(data['All Edge Cases']), \
        width, label="All Edge Cases")
    sub_plots.set_xticks(axis_ordered)
    sub_plots.set_xticklabels(data['Season'])
    sub_plots.set_ylabel('Number of Edge Cases')
    sub_plots.set_xlabel('Season')
    sub_plots.legend()
    fig.tight_layout()
    plt.show()


def playoffs_versus_season():
    """
    Plots %3PA and %3PM for regular season and playoffs
    in subplots.

    Args:
        None.

    Returns:
        A subplot of scatter plots comparing the %3PA
        with the %3PM.
    """
    plt.subplot(221)
    seaborn_plots_silent('Field_Goals_Attempted_3PA', False)
    plt.subplot(222)
    seaborn_plots_silent('Field_Goals_Attempted_3PA', True)
    plt.subplot(223)
    seaborn_plots_silent('Field_Goals_3P', False)
    plt.subplot(224)
    seaborn_plots_silent('Field_Goals_3P', True)
    plt.show()


def plot_win_compare_r_squared():
    fga_r_sq = win_compare_r_squared("Field_Goals_3P")
    fgm_r_sq = win_compare_r_squared("Field_Goals_Attempted_3PA")
    plt.subplot(121)
    plt.scatter(fga_r_sq.keys(), fga_r_sq.values())
    plt.xlabel('Season')
    plt.ylabel('R-squared')
    plt.title('R-Squared for %3PA and Win Percentage')
    plt.subplot(122)
    plt.scatter(fgm_r_sq.keys(), fgm_r_sq.values())
    plt.xlabel('Season')
    plt.ylabel('R-squared')
    plt.title('R-Squared for %3PM and Win Percentage')
    plt.show()


def interactive_map(team):
    """
    Generates interactive map based on team names (includes playoffs).

    Args:
        team: A string containing a team name from the NBA.

    Returns:
        An interactive plot with a dropdown to observe a NBA stat for
        a team over the scrapped  data sets.
    """
    team_summary_df = team_summary(team)
    fig = go.Figure()
    for column in team_summary_df.columns.to_list():
        fig.add_trace(
            go.Scatter(
                x = team_summary_df.index,
                y = team_summary_df[column],
                name = column
            )
        )

    button_initial = dict(label = 'Please Select One', method = 'update',
                      args = [{'title':'Please Select One',
                               'showlegend':True}])

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'visible': team_summary_df.columns.isin([column]),
                             'title': column,
                             'showlegend': True}])

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = [button_initial] + \
            list(team_summary_df.columns.map(lambda column: create_layout_button(column)))
            )
        ],
        yaxis_type="log"
    )
    fig.update_layout(
        title_text=f"{team} Team Summary",
        height=800
    )
    fig.show()
