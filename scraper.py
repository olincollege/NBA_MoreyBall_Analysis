from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import os, statistics

def get_shooting_reg_season():
    """
    Scrapes 10 seasons of shooting data from basketball-reference and
    converts it to CSV format.
    """
    for i in range(10,21):
        r = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_20{i}.html&div=div_team_shooting")
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.to_csv(f'Data/{i}')


def get_shooting_playoffs():
    """
    Scrapes 10 playoffs of shooting data during playoffs from 
    basketball-reference and converts it to CSV format.
    """
    for i in range(10,21):
        r = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fplayoffs%2FNBA_20{i}.html&div=div_opponent_shooting")
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.to_csv(f'Data/{i}p')

def convert_to_csv():
    """
    Takes plain text doc output of the last two functions and converts
    files to CSV format.
    """
    os.chdir('Data')
    files = os.listdir()
    for file in files:
        os.rename(file, f"20{file}")


def get_win_data(year):
    """
    Retrieves win-loss record data for a given year and returns a dictionary with
    team name and win-loss in a tuple.

    Args:
        year: an int representing the year of data to receive

    Returns: A pandas dataframe where the index is team name, first column is
    number of wins, and second is number of losses.
    """
    record = {}
    r = get(f"https://www.basketball-reference.com/leagues/NBA_{year}.html")
    soup = BeautifulSoup(r.content, 'html.parser')

    if year >= 2016:
        table_e = soup.find('table', attrs={'id':'confs_standings_E'})
        table_w = soup.find('table', attrs={'id':'confs_standings_W'})
        df_e = pd.read_html(str(table_e))[0]
        df_w = pd.read_html(str(table_w))[0]
    else:
        table_e = soup.find('table', attrs={'id':'divs_standings_E'})
        table_w = soup.find('table', attrs={'id':'divs_standings_W'})
        df_e = pd.read_html(str(table_e))[0]
        df_w = pd.read_html(str(table_w))[0]
    for i in range(0,df_w.shape[0]):
        key = df_e.iloc[i,0]
        if key[len(key)-8: len(key)] == "Division":
            continue
        else:
            record[df_e.iloc[i,0]] = (df_e.iloc[i,1], df_e.iloc[i,2])
            record[df_w.iloc[i,0]] = (df_w.iloc[i,1], df_w.iloc[i,2])
    
    if 'New Jersey Nets' in record.keys(): 
        record['Brooklyn Nets'] = record.pop('New Jersey Nets')

    record = dict(sorted(record.items()))
    record = pd.DataFrame.from_dict(record, orient='index')
    record.index = record.index.str.replace("*","")

    return record

def get_playoff_series_won(year):
    """
    Retrieves the number of series' won by each team for a single year
    in the playoffs.

    Args:
        year: an int that represents the year of data to retrieve

    Returns: A pandas dataframe where indices are team names, and the column
    is the number of playoffs series' won.
    """
    series_results = {}
    r = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fplayoffs%2FNBA_{year}_standings.html&div=div_expanded_standings")
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find('table', attrs={'id':'expanded_standings'})
    df = pd.read_html(str(data))[0]
    for i in range(0,df.shape[0]):
        record = df.iloc[i,2]
        dash = record.index('-')
        series_results[df.iloc[i,1]] = int(df.iloc[i,2][0:dash])//4
    
    series_results = pd.DataFrame.from_dict(series_results, orient='index')
    series_results.index = series_results.index.str.replace("*","")
    return series_results


def get_efg():
    """
    Scrapes eFG% for every team for each of the years  

    Returns: A pandas dataframe where indices are the year of team data collected
    (30 entries for 2010, 30 for 2011, etc.), and the column is eFG% of that 
    team. Note that team names are not referenced in the dataframe.
    """
    efgs = {}
    efg_year = []
    efg = []
    year_list = ['2010', '2011', '2012', '2013', \
        '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    for year in year_list:
        r = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{year}.html&div=div_misc_stats")
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find('table', attrs={'id':'misc_stats'})
        df = pd.read_html(str(data))[0]
        for i in range(0,df.shape[0]):
            efg.append(df.iloc[i,17])
            efg_year.append(year)
            
    df = pd.DataFrame(list(zip(efg_year, efg)), columns=['Year', 'eFG%'])
    return df
