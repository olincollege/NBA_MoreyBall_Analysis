from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import os

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
    team name and win-loss in a tuple..
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