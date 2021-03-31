import pandas as pd
import matplotlib.pyplot as plt
import os 

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
    Returns the cleaned data set.
    """
    data_set_size = len(data_set.columns) - 19
    readable_column_headers = ['nan'] + list(DATA_NAMES.keys()) + (['nan']*data_set_size)
    
    data_set.columns = readable_column_headers
    data_set = data_set.drop(columns = ['nan'])

    return data_set

def season_full_data(file_name):
    """
    Entire season data
    """
    data_set = pd.read_csv(f"Data/{file_name}")
    data_set.columns = data_set.iloc[1]
    data_set = data_set[2:-1]
    data_set['Team'] = data_set['Team'].str.replace("*","")

    return get_season_clean_csv(data_set)

def season_summary(file_name):
    """
    Get season summary for each year
    """
    data_set = pd.read_csv(f"Data/{file_name}")
    data_set.columns = data_set.iloc[1]
    data_set = data_set[-1:]
    data_set['Team'] = data_set['Team'].str.replace("*","")

    return get_season_clean_csv(data_set)

def team_summary(team):
    """
    Get team summary for each year
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

def season_summary_visual():
    """
    Trend over time of a certain stat
    """
    pass

def team_summary_visual():
    """
    Trend over time of a certain stat
    """
    pass

def compare_var_visual():
    """
    Compare two variables over time
    """
    pass

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
