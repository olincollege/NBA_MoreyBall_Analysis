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
        y_label: A string representing the desired y-label of the plot.
        title: A string representing the desired title of the plot.
    
    Returns:
        Plots a scatter of season summary of a nba stat.
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
        stat: A string representing the desired stat to pull data for
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


def win_compare(year,stat_nba, playoff, xlabel, ylabel, title):
    """
    Compares the win/loss record to a nba stat for all teams
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
        Plots a scatter of the win/loss record against a nba stat
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


def nba_stat_plot(stat_nba, playoff):
    """
    Genereats a box and whisker plot of a nba state over
    the scrapped data frame.

    Args:
        stat_nba: A string representing the desired stat to
        pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.
    
    Returns: 
        A box and whisker plot for the particularnba stat
    """
    df = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(df))
    plt.show()


def seaborn_plots_silent(stat_nba, playoff):
    """
    Genereats a box and whisker plot of a nba state over
    the scrapped data frame for subplots.

    Args:
        stat_nba: A string representing the desired stat to
        pull data for.
        playoff: A boolean representing whether to pull playoffs stats
        or regular season stats.
    
    Returns: 
        A box and whisker plot for the particular nba stat
        to be used in subplots.
    """
    df = nba_stat_summary(stat_nba, playoff)
    sns.boxplot(x="variable", y="value", data=pd.melt(df))


def efg_vs_3PA():
    """
    Creates a plot comparing the effective field goal values
    to the 3 point attempted values. 

    Args:
        None.
    
    Returns: 
        A boxplot comparing the effective field goal values
        with the 3 point attempted values.
    """
    efgs = get_efg()
    sns.boxplot(x="Year", y="eFG%", data=efgs)
    plt.show()


def playoff_3P_chart(year, playoffs):
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
    rects1 = ax.bar(x - width/2, threes_attempted, width, 
                    label="% Shots Attempted from 3PT")
    rects2 = ax.bar(x + width/2, threes_made, width, 
                    label="% 3PT Shots made")

    ax.set_ylabel('Percentage (as decimal)')
    ax.set_title(f'Three Point Shooting by Playoffs Outcome ({year})')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.show()


def edge_case_graph():
    """
    Generates bar graph to compare the edge case metric over
    the scarpped data frame. 

    Args: 
        None. 
    
    Returns: 
        A bar graph comparing the edge case metric. 

    1 Point is added to the "edge" metric during a season if a team that is
    top 5 in 3PA makes the playoffs. 
    1 point is subtracted if a team that is bottom 5 in 3PA makes the playoffs.
    """
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
    in subplots.

    Args:
        None.
    
    Returns: 
        A subplot of scatter plots comparing the %3PA
        with the %3PM.
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


def interactive_map(team):
    """
    Generates interactive map based on team names (includes playoffs).

    Args: 
        team: A string containing a team name from the NBA.

    Returns:
        An interactive plot with a dropdown to observe a nba state for
        a team over the scarpped data sets.
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
            buttons = [button_initial] + \
            list(df.columns.map(lambda column: create_layout_button(column)))
            )
        ],
         yaxis_type="log"       
    )
    fig.update_layout(
        title_text=f"{team} Team Summary",
        height=800
    )
    fig.show()

def edge_case():

    edge_numbers = ([0, 1, 2, 3, 4] * 11) * 2
    nba_paramters = (["Field_Goals_Attempled_3PA"] * 5 + \
        ['Field_Goals_3P'] * 5) * 11
    time = []
    for years in YEARS_LIST:
        time.append([years] * 10)
    flat_time = [item for sublist in time for item in sublist]

    df = pd.DataFrame()
    df['date'] = edge_numbers
    df['Reason'] = nba_paramters
    df['name'] = flat_time 

    scores = []
    for years in YEARS_LIST:
        data = playoff_round_3P(str(years), False)
        for i in range(0,len(data)):
            scores.append(data[i][0])
            scores.append(data[i][1])

    df['Task'] = scores
    
    # split df by names
    names = df['name'].unique().tolist()
    dates = df['date'].unique().tolist()

    dfs = {}

    # dataframe collection grouped by names
    for name in names:
        #print(name)
        dfs[name]=pd.pivot_table(df[df['name']==name],
                                values='Task',
                                index=['date'],
                                columns=['Reason'],
                                aggfunc=np.sum)

    # plotly start 
    fig = go.Figure()

    # get column names from first dataframe in the dict
    colNames = list(dfs[list(dfs.keys())[0]].columns)
    #xValues=

    # one trace for each column per dataframe: AI and RANDOM
    for col in colNames:
        fig.add_trace(go.Bar(x=dates,
                                visible=True,
                                #name=col
                    )
                )

    # menu setup    
    updatemenu= []

    # buttons for menu 1, names
    buttons=[]

    # create traces for each Reason: AI or RANDOM
    for df in dfs.keys():
        buttons.append(dict(method='update',
                            label=df,
                            visible=True,
                            args=[#{'visible':True},
                                #{'x':[dfs[df]['AI'].index, dfs[df]['RANDOM'].index]},
                                {'y':[dfs[df]['Field_Goals_Attempled_3PA'].values, dfs[df]['Field_Goals_3P'].values]}])
                    )

    # buttons for menu 2, reasons
    b2_labels = colNames

    # matrix too feed all visible arguments for all traces
    # so that they can be shown or hidden by choice
    b2_show = [list(b) for b in [e==1 for e in np.eye(len(b2_labels))]]
    buttons2=[]
    buttons2.append({'method': 'update',
                    'label': 'All',
                    'args': [{'visible': [True]*4}]})

    # create buttons to show or hide
    for i in range(0, len(b2_labels)):
        buttons2.append(dict(method='update',
                            label=b2_labels[i],
                            args=[{'visible':b2_show[i]}]
                            )
                    )

    # add option for button two to hide all
    buttons2.append(dict(method='update',
                            label='None',
                            args=[{'visible':[False]*4}]
                            )
                    )

    # some adjustments to the updatemenus
    updatemenu=[]
    your_menu=dict()
    updatemenu.append(your_menu)
    your_menu2=dict()
    updatemenu.append(your_menu2)
    updatemenu[1]
    updatemenu[0]['buttons']=buttons
    updatemenu[0]['direction']='down'
    updatemenu[0]['showactive']=True
    updatemenu[1]['buttons']=buttons2
    updatemenu[1]['y']=0.6

    fig.update_layout(showlegend=False, updatemenus=updatemenu)
    fig.show()
