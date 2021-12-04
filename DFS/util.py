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
    dk_salary = pd.read_csv('DKSalaries 12_4_21.csv')
    dk_salary = dk_salary[['Roster Position', 'Position', 'Name', 'Salary', 'TeamAbbrev']]
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
    team_cities = []
    team_nicks = []
    team_names = []
    team_abvs = []
    for team in tm:
        team_name = team.find("td", class_ = "left team-cell")
        team_name = team_name.text
        team_abbrev = team_name[0:3]
        team_abvs.append(team_abbrev)
        team_city = team_name[3:len(team_name)].rsplit(' ', 1)[0]
        team_cities.append(team_city)
        team_nick = team_name[3:len(team_name)].split()[-1]
        team_nicks.append(team_nick)
        team_name = team_name[3:len(team_name)]
        team_names.append(team_name)
        

    pg_s = soup.find_all("tr", class_ = "GC-0 PG")
    pgs_s = []
    for pg in pg_s:
        pgfp_allowed_season = pg.find_all("td", class_ = "center")[-1].text
        pgs_s.append(pgfp_allowed_season)
    pg_7 = soup.find_all("tr", class_ = "GC-7 PG")
    pgs_7 = []
    for pg in pg_7:
        pgfp_allowed_seven = pg.find_all("td", class_ = "center")[-1].text
        pgs_7.append(pgfp_allowed_seven)
    sg_s = soup.find_all("tr", class_ = "GC-0 SG")
    sgs_s = []
    for sg in sg_s:
        sgfp_allowed_season = sg.find_all("td", class_ = "center")[-1].text
        sgs_s.append(sgfp_allowed_season)
    sg_7 = soup.find_all("tr", class_ = "GC-7 SG")
    sgs_7 = []
    for sg in sg_7:
        sgfp_allowed_seven = sg.find_all("td", class_ = "center")[-1].text
        sgs_7.append(sgfp_allowed_seven)
    sf_s = soup.find_all("tr", class_ = "GC-0 SF")
    sfs_s = []
    for sf in sf_s:
        sffp_allowed_season = sf.find_all("td", class_ = "center")[-1].text
        sfs_s.append(sffp_allowed_season)
    sf_7 = soup.find_all("tr", class_ = "GC-7 SF")
    sfs_7 = []
    for sf in sf_7:
        sffp_allowed_seven = sf.find_all("td", class_ = "center")[-1].text
        sfs_7.append(sffp_allowed_seven)
    pf_s = soup.find_all("tr", class_ = "GC-0 PF")
    pfs_s = []
    for pf in pf_s:
        pffp_allowed_season = pf.find_all("td", class_ = "center")[-1].text
        pfs_s.append(pffp_allowed_season)
    pf_7 = soup.find_all("tr", class_ = "GC-7 PF")
    pfs_7 = []
    for pf in pf_7:
        pffp_allowed_seven = pf.find_all("td", class_ = "center")[-1].text
        pfs_7.append(pffp_allowed_seven)
    c_s = soup.find_all("tr", class_ = "GC-0 C")
    cs_s = []
    for c in c_s:
        cfp_allowed_season = c.find_all("td", class_ = "center")[-1].text
        cs_s.append(cfp_allowed_season)
    c_7 = soup.find_all("tr", class_ = "GC-7 C")
    cs_7 = []
    for c in c_7:
        cfp_allowed_seven = c.find_all("td", class_ = "center")[-1].text
        cs_7.append(cfp_allowed_seven)
    dvp = pd.DataFrame({'team_abbreviation': team_abvs, 'team_city': team_cities, 'team_nicknames': team_nicks, 'team_name': team_names, 'pg-season' : pgs_s, 'pg-seven' : pgs_7, 'sg-season': sgs_s, 'sg_seven' : sgs_7, 'sf-season': sfs_s, 'sf_seven' : sfs_7,'pf-season': pfs_s, 'pf_seven' : pfs_7, 'C-season': cs_s, 'C_seven' : cs_7})
    return(dvp)
    
def input_df():
    opp = get_opponents()
    dk_salary = get_player_id()
    team_dvp = dvp()
    team_dict = {team_dvp['team_nicknames'][i]: team_dvp['team_abbreviation'][i] for i in range(len(team_dvp['team_abbreviation']))}
    for key in team_dict.keys():
        opp = opp.replace(key, team_dict[key])
    
    home_opp = opp
    home_opp = home_opp.rename(columns = {'away team' : 'OppAbbrev'})
    home_opp['home_flag'] = 1
    
    dk_salary = pd.merge(left = dk_salary, right = home_opp, left_on = 'TeamAbbrev', right_on = 'home team', how = 'left')
    away_opp = opp
    away_opp = away_opp.rename(columns = {'home team' : 'OppAbbrev'})
    away_opp['home_flag'] = 0
    dk_salary = pd.merge(left = dk_salary, right = away_opp, left_on = 'TeamAbbrev', right_on = 'away team', how = 'left')
    dk_salary['OppAbbrev'] = dk_salary['OppAbbrev_x'].fillna(dk_salary['OppAbbrev_y'])
    dk_salary['home_flag'] = dk_salary['home_flag_x'].fillna(dk_salary['home_flag_y'])
    dk_salary = dk_salary[['Roster Position', 'Position', 'Name', 'Salary', 'TeamAbbrev', 'player_id', 'OppAbbrev', 'home_flag']]
    dk_salary = pd.merge(left = dk_salary, right = team_dvp, left_on = 'OppAbbrev', right_on = 'team_abbreviation', how = 'left')
    return(dk_salary)
dk_salary = input_df()