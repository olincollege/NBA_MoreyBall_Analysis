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