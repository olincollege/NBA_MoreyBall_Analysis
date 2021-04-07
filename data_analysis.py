import pandas as pd
import matplotlib.pyplot as plt
import os, operator, statistics
from scraper import get_win_data, get_playoff_series_won

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
    Get file names 
    """
    owd = os.getcwd()
    names = os.listdir(os.chdir('Data'))
    os.chdir(owd)
    return names


def get_season_clean_csv(data_set):
    """
    Clean all the data and drops the rest of the columns. 

    Returns: The cleaned data set as a pandas df.
    """
    data_set_size = len(data_set.columns) - 19
    readable_column_headers = ['nan'] + list(DATA_NAMES.keys()) + (['nan']*data_set_size)
    
    data_set.columns = readable_column_headers
    data_set = data_set.drop(columns = ['nan'])

    return data_set


def season_full_data(year, playoff):
    """
    Args:
        year: A string representing the year of data to be returned
        playoff: A boolean representing whether to clean playoff or regular
        season data.

    Returns: cleaned up full season data to be inputted into other
    functions. 
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
    Get season summary stats for each year

    This stat will be the league average of each stat listed in DATA_NAMES
    for all teams.

    Args:
        year: A string representing the desired year of data
        playoff: A boolean representing whether to pull playoff data or
        regular season.
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
    Pulls data for a single stat for every team over the last 10 seasons.

    Returns: a pandas dataframe where indices represent different teams and
    column header represents the season.
    """
    df = pd.DataFrame(columns=YEARS_LIST)

    for years in YEARS_LIST:
        season_full =  season_full_data(years, playoff)
        df[years] = pd.to_numeric(season_full[stat_nba])

    return df


def team_summary(team):
    """
    Get team summary stats for each year from the scraped CSV.

    Team summary stats include yearly averages for all stats listed in
    DATA_NAMES.

    Args:
        team: A string representing the name of the team to pull data for.
    """
    file_names = sorted(get_file_names())
    team_summary_full = pd.DataFrame(columns = list(DATA_NAMES.keys()), index = file_names)

    for files in file_names:
        data_set = season_full_data(files, False)
        if team in data_set.Team.values:
            data_set.set_index("Team", inplace=True)
            data_set.head()
            team_summary_full.loc[files] = data_set.loc[team]
    
    team_summary_full.pop("Team")
    team_summary_full.index = team_summary_full.index.str.replace('.csv', '', regex=True)

    return team_summary_full.dropna()


def edge_cases_metric():
    """
    For each season, calculated edge case metric.
    1 Point is added to the "edge" metric during a season if a team that is
    top 5 in 3PA makes the playoffs. 1 point is subtracted if a team that is
    bottom 5 in 3PA makes the playoffs.

    Returns: Dictionary where key is an int representing the year and the
    value is the number of edge-cases during that year.
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


def playoff_round_3P(year, playoffs):
    """
    Compares playoffs outcome to % of shots attempted
    from 3PT and % of three points attempted made.

    Args:
        year: an int representing the year to compare data for
        playoffs: a boolean representing whether to compare outcome to 
        team shooting data in the playoffs or regular season

    Returns: a dictionary where the key is the number of playoffs rounds
    won and the key is a list where the 0th element is %3PA and the 1st is
    %3PM
    """
    playoffs = get_playoff_series_won(year)
    d = playoffs.to_dict()[0]
    # Accounting forhanges in team names
    if 'New Jersey Nets' in d:
        d['Brooklyn Nets'] = d.pop('New Jersey Nets')
    if 'Charlotte Bobcats' in d:
        d['Charlotte Hornets'] = d.pop('Charlotte Bobcats')
    if 'New Orleans Hornets' in d:
        d['New Orleans Pelicans'] = d.pop('New Orleans Hornets')

    keys = d.keys()
    season_data = season_full_data(year, playoffs)
    playoff_data = {}

    for i in range(season_data.shape[0]):
        name = season_data.iloc[i,1]
        if name not in list(d.keys()):
            continue
        else:
            if d[name] in playoff_data:
                playoff_data[d[name]][0].append(float(season_data.iloc[i,11]))
                playoff_data[d[name]][1].append(float(season_data.iloc[1,17]))
            else:
                playoff_data[d[name]] = [[float(season_data.iloc[i,11])], [float(season_data.iloc[i,17])]]

    for i in range(0,5):
        playoff_data[i][0] = statistics.mean(playoff_data[i][0])
        playoff_data[i][1] = statistics.mean(playoff_data[i][1])

    return dict(sorted(playoff_data.items()))
