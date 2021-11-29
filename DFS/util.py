# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 13:58:14 2021

@author: thyang
"""
"""
Get players playing today + salary
"""
from nba_api.stats.static import players
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_salary():
    dk_salary = pd.read_csv('DKSalaries 11_26_21.csv')
    dk_salary = dk_salary[['Roster Position', 'Name', 'Salary', 'TeamAbbrev']]
    return dk_salary

"""
Get Opponents and PlayerId
"""
def get_player_id():
    dk_salary = get_salary()
    names = dk_salary['Name']
    player_ids = []
    for name in names:
        try:
            player = players.find_players_by_full_name(name)[0]
            player_id = player['id']
        except:
            print(name + " is missing")
            player_id = 0
        player_ids.append(player_id)
    dk_salary['player_id'] = player_ids
    return dk_salary


def get_opponents():
    URL = "https://sportsdata.usatoday.com/basketball/nba/scores"
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, "html.parser")
    initial_names = soup.find_all("span", class_ = "class-1fB7hU-")
    team_names = []
    for name in initial_names:
        name = name.text
        name = re.sub('[^a-zA-Z]+', '', name)
        team_names.append(name)
    home_team = team_names[1::2]
    away_team = team_names[::2]
    opponents = pd.DataFrame({'home team' : home_team, 'away team': away_team})
    return(opponents)
def dvp():
    URL = "https://www.fantasypros.com/daily-fantasy/nba/draftkings-defense-vs-position.php"
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, "html.parser")
    tm = soup.find_all("tr", class_ = "GC-0 TM")
    team_names = []
    for team in tm:
        team_name = team.find("td", class_ = "left team-cell")
        team_name = team_name.text
        team_names.append(team_name)
    print(team_names)
    pg_s = soup.find_all("tr", class_ = "GC-0 PG")
    pgs_s = []
    for pg in pg_s:
        pgfp_allowed_season = pg.find_all("td", class_ = "center")[-1].text
        pgs_s.append(pgfp_allowed_season)
    print(pgs_s)
print(dvp())    