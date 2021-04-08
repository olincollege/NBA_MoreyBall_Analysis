"""
Data scrapper functions to collect data from basketball-reference.com
"""

import os
import pandas as pd
from requests import get
from bs4 import BeautifulSoup


def get_shooting_reg_season():
    """
    Scrapes 10 seasons of shooting data from basketball-reference.com
    and converts it to CSV format.

    Args:
        None.

    Returns:
        Creates .csv files in folder 'Data'.
    """
    for i in range(10,21):
        raw_data = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=\
            bbr&url=%2Fleagues%2FNBA_20{i}.html&div=div_team_shooting")
        html_parser = BeautifulSoup(raw_data.content, 'html.parser')
        table_finder = html_parser.find('table')
        shotting_data_df = pd.read_html(str(table_finder))[0]
        shotting_data_df.to_csv(f'Data/{i}')


def get_shooting_playoffs():
    """
    Scrapes 10 playoffs of shooting data during playoffs from
    basketball-reference.com and converts it to CSV format.

    Args:
        None.

    Returns:
        Creates .csv files in folder 'Data'.
    """
    for i in range(10,21):
        raw_data = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&\
            site=bbr&url=%2Fplayoffs%2FNBA_20{i}.html&div=div_opponent_shooting")
        html_parser = BeautifulSoup(raw_data.content, 'html.parser')
        table_finder = html_parser.find('table')
        shotting_data_df = pd.read_html(str(table_finder))[0]
        shotting_data_df.to_csv(f'Data/{i}p')


def convert_to_csv():
    """
    Takes plain text doc output of the get_shooting() and converts
    files to CSV format.

    Args:
        None.

    Returns:
        Fits the names of the files to match the year they belong to.
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
        year: An int representing the year of data to receive

    Returns:
        A Pandas data frame where the index is the team name, the first column is
        the number of wins and the second is the number of losses.
    """
    record = {}
    raw_data = get(f"https://www.basketball-reference.com/leagues/NBA_{year}.html")
    soup = BeautifulSoup(raw_data.content, 'html.parser')

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
    Retrieves the number of game series' won by each team for
    a single year in the playoffs.

    Args:
        year: An int that represents the year of data to retrieve.

    Returns:
        A Pandas data frame where indices are team names, and the column
        is the number of playoffs series' won.
    """
    series_results = {}
    raw_data = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2\
        Fplayoffs%2FNBA_{year}_standings.html&div=div_expanded_standings")
    soup = BeautifulSoup(raw_data.content, 'html.parser')
    data = soup.find('table', attrs={'id':'expanded_standings'})
    series_won_df = pd.read_html(str(data))[0]
    for i in range(0,series_won_df.shape[0]):
        record = series_won_df.iloc[i,2]
        dash = record.index('-')
        series_results[series_won_df.iloc[i,1]] = int(series_won_df.iloc[i,2][0:dash])//4

    series_results = pd.DataFrame.from_dict(series_results, orient='index')
    series_results.index = series_results.index.str.replace("*","")
    return series_results


def get_efg():
    """
    Scrapes eFG% for every team for each of the years
    from basket_reference.com.

    Args:
        None.

    Returns:
        A Pandas data frame where indices are the year of team data collected,
        and the column is eFG% of that team.

    Note that team names are not referenced in the data frame.
    """
    efg_year = []
    efg = []
    year_list = ['2010', '2011', '2012', '2013', \
        '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    for year in year_list:
        raw_data = get(f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url\
            =%2Fleagues%2FNBA_{year}.html&div=div_misc_stats")
        soup = BeautifulSoup(raw_data.content, 'html.parser')
        data = soup.find('table', attrs={'id':'misc_stats'})
        efg_df = pd.read_html(str(data))[0]
        for i in range(0,efg_df.shape[0]):
            efg.append(efg_df.iloc[i,17])
            efg_year.append(year)

    efg_df_extract = pd.DataFrame(list(zip(efg_year, efg)), columns=['Year', 'eFG%'])
    return efg_df_extract
