import pandas as pd
import matplotlib.pyplot as plt
import os, operator
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


def get_file_names():
    """
    Get file names
    """
    owd = os.getcwd()
    names = os.listdir(os.chdir('Data'))
    os.chdir(owd)
    return names


def data_var_def():
    """
    Prints all the headers of the data and what they mean
    in a clean styled table
    """
    data_dictionary = pd.DataFrame(DATA_NAMES.items(), columns=["CSV Headers", "Meaning"])
    data_dictionary_style = data_dictionary.style.set_properties(**{'text-align': 'left'})
    data_dictionary_style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    return data_dictionary_style


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


def team_summary(team):
    """
    Get team summary stats for each year from the scraped CSV.

    Team summary stats include yearly averages for all stats listed in
    DATA_NAMES.

    Args:
        team: A string representing the name of the team to pull data for.
    """
    file_names = get_file_names()
    team_summary_full = pd.DataFrame(columns = list(DATA_NAMES.keys()), index = file_names)

    for files in file_names:
        data_set = season_full_data(files)
        if team in data_set.Team.values:
            data_set.set_index("Team", inplace=True)
            data_set.head()
            team_summary_full.loc[files] = data_set.loc[team]
    
    team_summary_full.pop("Team")

    return team_summary_full.dropna()


def season_summary_visual(stat, playoff, y_label, title):
    """
    Trend over time of the league average of a single stat

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
    Trend over time of a certain stat
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


def compare_var_visual():
    """
    Compare two variables over time
    """
    pass


def edge_cases_metric():
    """
    For each season, calculated edge case metric.
    1 Point is added to the "edge" metric during a season if a team that is
    top 5 in 3PA makes the playoffs. 1 point is subtracted if a team that is
    bottom 5 in 3PA makes the playoffs.
    """
    edges = {}
    
    for i in range(10,20):
        data = season_full_data(f"20{i}.csv")
        playoffs = get_playoff_series_won(f"20{i}").keys()
        percents = dict(zip(data.iloc[:,1],data.iloc[:,11]))
        sorted_percents = sorted(percents.items(), key=operator.itemgetter(1))
        bottom_five = sorted_percents[0:5]
        top_five = sorted_percents[-5:-1]
        top_five.append(sorted_percents[0])
        for j in range(0,5):
            metric = 0
            if bottom_five[j][0] in playoffs:
                print(bottom_five[j][0], i, "bottom")
                metric -= 1
            if top_five[j][0] in playoffs:
                print(top_five[j][0], i, "top")
                metric += 1
        edges[i] = metric
    return edges

"""
def morey_ball_analysis(year, playoff):



    team = clean_data_set["Rank"]
    field_goal_percent = clean_data_set["Field_Goals_3P"]

    plt.plot(team, field_goal_percent, ".")

    print(data_set)

  
    # Uncomment the next code line and modify to plot the data appropriately.
    # Then delete these comment lines.
    plt.plot(forces, power_output, ".")
    
    # In the following lines, replace the strings with appropriate labels.
    plt.xlabel("Force on Accelerator (Lbs)")
    plt.ylabel("Horsepower (Hp)")
    plt.title(f"Effect of Force on Accelerator (Lbs) on the Engine Horsepower (Hp) using a {engine_type} Engine")
    plt.show()
"""
