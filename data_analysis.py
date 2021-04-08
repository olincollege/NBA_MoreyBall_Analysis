"""
Functions to analyse and select data from scrapped files.
"""
import os
import operator
import statistics
import pandas as pd
import numpy as np
from scraper import get_playoff_series_won, get_win_data

pd.set_option('display.max_colwidth', 0)

DATA_NAMES = {
    'Rank': 'Rank of Team',
    'Team': 'Team Name (w/ asterisk if they made playoff)',
    'Games_Played' : 'Number of Games Played',
    'Minutes_Played': 'Minutes Played by Team',
    'Field_Goal_Percent': 'Field Goal Percentage',
    'Average_Distance': ' Average Distance of Field Goals Attempted',
    'Field_Goals_Attempled_2PA': 'Percent of Field Goals Attempted that were 2 Point Attempts',
    '2PA_0-3': 'Field Goals Attempted in the range of 0 - 3 fts from the hoop (2 Points)',
    '2PA_3-10':'Field Goals Attempted in the range of 3 - 10 fts from the hoop (2 Points)',
    '2PA_10-16': 'Field Goals Attempted in the range of 10 - 16 fts from the hoop (2 Points)',
    '2PA_16+': 'Field Goals Attempted above 16 fts from the hoop (2 Points)',
    'Field_Goals_Attempled_3PA': 'Percent of Field Goals Attempted that were 3 Point Attempts',
    'Field_Goals_2P': 'Percent of Field Goals that were 2 Points',
    '2P_0-3': 'Field Goals in the range of 0 - 3 fts from the hoop (2 Points)',
    '2P_0-6': 'Field Goals in the range of 3 - 10 fts from the hoop (2 Points)',
    '2P_10-16': 'Field Goals in the range of 10 - 16 fts from the hoop (2 Points)',
    '2P16+': 'Field Goals above 16 fts from the hoop (2 Points)',
    'Field_Goals_3P': 'Percent of Field Goals that were 3 Points'
}

YEARS_LIST = ['2010','2011','2012','2013','2014', \
    '2015','2016','2017','2018','2019','2020', ]

def get_file_names():
    """
    Get file names from the folder 'Data' in the repo.

    Args:
        None.

    Returns:
        List of strings containing all the names of the files.
    """
    owd = os.getcwd()
    names = os.listdir(os.chdir('Data'))
    os.chdir(owd)
    return names


def get_season_clean_csv(data_set):
    """
    Cleans all the data and drops the rest of the columns
    collected from Basketball-Reference.com.

    Args:
        data_set: Pandas dataframe with data from Basketball-Reference.com.

    Returns:
        A Pandas data frame with no empty data points, and excess
        columns deleted.
    """
    data_set_size = len(data_set.columns) - 19
    readable_column_headers = ['nan'] + list(DATA_NAMES.keys()) + \
        (['nan']*data_set_size)

    data_set.columns = readable_column_headers
    data_set = data_set.drop(columns = ['nan'])

    return data_set


def season_full_data(year, playoff):
    """
    Gets the full data for any season in the scrapped data.

    Args:
        year: An int representing the year of data to be returned.
        playoff: A boolean representing whether to clean playoff or regular
        season data.

    Returns:
        A cleaned-up Pandas data frame with full-season data.
    """
    if playoff:
        data_set = pd.read_csv(f"Data/{year}p.csv")
    else:
        data_set = pd.read_csv(f"Data/{year}.csv")
    data_set.columns = data_set.iloc[1]
    data_set = data_set[2:-1]
    data_set['Team'] = data_set['Team'].str.replace("*","")

    return get_season_clean_csv(data_set)


def season_summary(year, playoff):
    """
    Get season summary stats for each year.

    Args:
        year: An int representing the desired year of data.
        playoff: A boolean representing whether to pull playoff data or
        regular season.

    Returns:
        A cleaned-up Pandas dataframe with season summary data.

    This stat will be the league average of each stat listed in DATA_NAMES
    for all teams.
    """
    if playoff:
        data_set = pd.read_csv(f"Data/{year}p.csv")
    else:
        data_set = pd.read_csv(f"Data/{year}.csv")
    data_set.columns = data_set.iloc[1]
    data_set = data_set[-1:]
    data_set['Team'] = data_set['Team'].str.replace("*","")

    return get_season_clean_csv(data_set)


def nba_stat_summary(stat_nba, playoff):
    """
    Pulls data for a single stat for every team over the scrapped data.

    Args:
        stat_nba: A string of the nba stat to pull data on.
        playoff: A boolean representing whether to pull playoff data or
        regular season.

    Returns:
        A Pandas dataframe where indices represent different teams and
        column header represents the season.
    """
    stat_summary_df = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        season_full =  season_full_data(years, playoff)
        stat_summary_df[years] = pd.to_numeric(season_full[stat_nba])

    return stat_summary_df


def team_summary(team):
    """
    Get team summary stats for each year from the scrapped CSV.

    Args:
        team: A string representing the name of the team to pull data for.

    Returns:
        A Pandas dataframe containing the team summary from
        scarpped CSV.

    Team summary stats include yearly averages for all stats listed in
    DATA_NAMES.
    """
    file_names = sorted(get_file_names())
    team_summary_full = pd.DataFrame(columns = list(DATA_NAMES.keys()),
        index = file_names)

    for files in file_names:
        data_set = season_full_data(files[:-4], False)
        if team in data_set.Team.values:
            data_set.set_index("Team", inplace=True)
            data_set.head()
            team_summary_full.loc[files] = data_set.loc[team]

    team_summary_full.pop("Team")
    team_summary_full.index = team_summary_full.index.str.replace('.csv'
        ,'', regex=True)

    return team_summary_full.dropna()


def edge_cases_metric():
    """
    Calculates the edge metric for each season.

    Args:
        None.

    Returns:
        A dictionary where the key is an int representing the year and the
        value is the number of edge cases during that year.

    1 Point is added to the "edge" metric during a season if a team that is
    Top 5 in 3PA makes the playoffs.
    1 point is subtracted if a team that is Bottom 5 in 3PA makes the playoffs.
    """
    edges = {}

    for i in range(10,20):
        data = season_full_data(f"20{i}", False)
        playoffs = list(get_playoff_series_won(f"20{i}").to_dict()[0].keys())
        percents = dict(zip(data.iloc[:,1],data.iloc[:,11]))
        sorted_percents = sorted(percents.items(), key=operator.itemgetter(1))
        bottom_five = sorted_percents[0:5]

        top_five = sorted_percents[-6:-1]

        top_five.append(sorted_percents[0])
        for j in range(0,5):
            metric = 0
            if bottom_five[j][0] in playoffs:
                metric -= 1
            if top_five[j][0] in playoffs:
                metric += 1
        edges[i] = metric
    return edges


def playoff_round_3p(year, playoff):
    """
    Compares playoffs outcome to % of shots attempted
    from 3PT and % of three points attempted made.

    Args:
        year: An int representing the year to compare data for.
        playoffs: A boolean representing whether to compare outcome to
        team shooting data in the playoffs or regular season.

    Returns:
        A dictionary where the key is the number of playoffs rounds
        won and the key is a list where the 0th element is %3PA and the 1st is
        %3PM
    """
    playoffs = get_playoff_series_won(year)
    dic_playoff = playoffs.to_dict()[0]
    # Accounting forhanges in team names
    if 'New Jersey Nets' in dic_playoff:
        dic_playoff['Brooklyn Nets'] = dic_playoff.pop('New Jersey Nets')
    if 'Charlotte Bobcats' in dic_playoff:
        dic_playoff['Charlotte Hornets'] = dic_playoff.pop('Charlotte Bobcats')
    if 'New Orleans Hornets' in dic_playoff:
        dic_playoff['New Orleans Pelicans'] = dic_playoff.pop('New Orleans Hornets')

    season_data = season_full_data(year, playoff)
    playoff_data = {}

    for i in range(season_data.shape[0]):
        name = season_data.iloc[i,1]
        if name not in list(dic_playoff.keys()):
            continue
        if dic_playoff[name] in playoff_data:
            playoff_data[dic_playoff[name]][0].append(float(season_data.iloc[i,11]))
            playoff_data[dic_playoff[name]][1].append(float(season_data.iloc[1,17]))
        else:
            playoff_data[dic_playoff[name]] = [[float(season_data.iloc[i,11])],
            [float(season_data.iloc[i,17])]]

    for i in range(0,5):
        playoff_data[i][0] = statistics.mean(playoff_data[i][0])
        playoff_data[i][1] = statistics.mean(playoff_data[i][1])

    return dict(sorted(playoff_data.items()))


def win_compare_r_squared(stat_nba):
    """
    Compares the win/loss record to a NBA stat and outputs
    its correlation-coefficient for scrapped data.

    Args:
        stat_nba: A string of the nba stat to pull data on.

    Returns:
        A dictionary with keys as years and the values as the
        r^2 values.
    """
    stat_nba_df = pd.DataFrame(columns=YEARS_LIST)
    print(f"R^2 values for {stat_nba}")
    for years in YEARS_LIST:
        win_data = list(get_win_data(int(years)).iloc[:,0])
        games_played = int(season_summary(years, False).iloc[:,2])
        stat_nba_df[years] = [int(i) for i in win_data]
        stat_nba_df[years] = stat_nba_df[years].div(games_played).round(2)

    stat_nba_df.index = get_win_data(int(2010)).index
    nba_stat = nba_stat_summary(stat_nba, False)
    nba_stat.index = get_win_data(int(2010)).index

    r_squared_dict = {}
    for year in YEARS_LIST:
        stat_values = nba_stat[str(year)]
        win_values = stat_nba_df[str(year)]
        corr_matrix = np.corrcoef(win_values, stat_values)
        corr_xy = corr_matrix[0,1]
        r_sq = corr_xy**2
        r_squared_dict[year]: r_sq
    return r_squared_dict
    