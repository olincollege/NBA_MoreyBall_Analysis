"""
Data scrapper functions to collect data from basketball-reference.com
"""

import os, shutil
import pandas as pd
from tqdm import tqdm
from requests import get
from bs4 import BeautifulSoup


def run_scraper():
    with tqdm(total = 6, desc="Running Scraper") as pbar:
        pbar.update(1)
        get_shooting_playoffs()
        pbar.update(1)
        get_shooting_reg_season()
        pbar.update(1)
        get_win_data()
        pbar.update(1)
        get_playoff_series_won()
        pbar.update(1)
        get_efg()
        pbar.update(1)
        print("Scraper done running")


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
        raw_data = get("https://widgets.sports-reference.com/wg.fcgi?css=1&site="+
            f"bbr&url=%2Fleagues%2FNBA_20{i}.html&div=div_team_shooting")
        html_parser = BeautifulSoup(raw_data.content, 'html.parser')
        table_finder = html_parser.find('table')
        shooting_data_df = pd.read_html(str(table_finder))[0]
        shooting_data_df.to_csv(f'Data/season_shooting/20{i}.csv')


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
        raw_data = get("https://widgets.sports-reference.com/wg.fcgi?css=1&" + \
            f"site=bbr&url=%2Fplayoffs%2FNBA_20{i}.html&div=div_opponent_shooting")
        html_parser = BeautifulSoup(raw_data.content, 'html.parser')
        table_finder = html_parser.find('table')
        shooting_data_df = pd.read_html(str(table_finder))[0]
        shooting_data_df.to_csv(f'Data/season_shooting/20{i}p.csv')


def get_win_data():
    """
    Retrieves win-loss record data for a given year and returns a dictionary with
    team name and win-loss in a tuple.

    Args:
        year: An int representing the year of data to receive

    Returns:
        A Pandas data frame where the index is the team name, the first column is
        the number of wins and the second is the number of losses.
    """
    for i in range(10,21):
        year = int(f"20{i}")
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
        for j in range(0,df_w.shape[0]):
            key = df_e.iloc[j,0]
            if key[len(key)-8: len(key)] == "Division":
                continue
            record[df_e.iloc[j,0]] = (df_e.iloc[j,1], df_e.iloc[j,2])
            record[df_w.iloc[j,0]] = (df_w.iloc[j,1], df_w.iloc[j,2])

        if 'New Jersey Nets' in record.keys():
            record['Brooklyn Nets'] = record.pop('New Jersey Nets')

        record = dict(sorted(record.items()))
        record = pd.DataFrame.from_dict(record, orient='index')
        record.index = record.index.str.replace("*","", regex=False)

        record.to_csv(f'Data/win-loss/all_records_{year}.csv')


def get_playoff_series_won():
    """
    Retrieves the number of game series' won by each team for
    a single year in the playoffs.

    Args:
        year: An int that represents the year of data to retrieve.

    Returns:
        A Pandas data frame where indices are team names, and the column
        is the number of playoffs series' won.
    """
    for i in range(10,21):
        series_results = {}
        raw_data = get("https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&" +
                        f"url=%2Fplayoffs%2FNBA_20{i}_standings.html&div=div_expanded_standings")
        soup = BeautifulSoup(raw_data.content, 'html.parser')
        data = soup.find('table')
        series_won_df = pd.read_html(str(data))[0]
        for j in range(0,series_won_df.shape[0]):
            record = series_won_df.iloc[j,2]
            dash = record.index('-')
            series_results[series_won_df.iloc[j,1]] = int(series_won_df.iloc[j,2][0:dash])//4

        series_results = pd.DataFrame.from_dict(series_results, orient='index')
        series_results.index = series_results.index.str.replace("*","", regex=False)
        series_results.to_csv(f'Data/playoffs_outcome/playoffs_20{i}.csv')


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
    for i in range(10,21):
        year = f"20{i}"
        raw_data = get("https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&" +
                        f"url=%2Fleagues%2FNBA_{year}.html&div=div_misc_stats")
        soup = BeautifulSoup(raw_data.content, 'html.parser')
        data = soup.find('table', attrs={'id':'misc_stats'})
        efg_df = pd.read_html(str(data))[0]
        for j in range(0,efg_df.shape[0]):
            efg.append(efg_df.iloc[j,17])
            efg_year.append(year)

    efg_df_extract = pd.DataFrame(list(zip(efg_year, efg)), columns=['Year', 'eFG%'])
    efg_df_extract.to_csv('Data/efg/efg.csv')
