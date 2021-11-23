# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 09:44:59 2021
Forecasting:
Using seasonal data to create a forecast for a player's performance versus opponent
@author: pjyang4
"""

"""
Get Seasonal Data

"""
from nba_api.stats.endpoints import playergamelogs
from datetime import datetime
import numpy as np

START_DATE = '2021-10-19'
today = datetime.today().strftime('%Y-%m-%d')


def dfk_fantasy_pts(player):
    player['dbl_dbl'] = np.where(((player['PTS'] >= 10) & (player['REB'] >= 10)) | ((player['PTS'] >= 10) & (player['AST'] >= 10)) | ((player['REB'] >= 10) & (player['AST'] >= 10)), 1, 0)
    player['trp_dbl'] = np.where(((player['PTS'] >= 10) & (player['REB'] >= 10) & (player['AST'] >= 10)),1,0)
    fantasy_pts = player['PTS'] + .5*player['FG3M'] + 1.25*player['REB'] + 1.5 * player['AST'] + 2*player['BLK'] + 2*player['STL'] - 0.5*player['TOV'] + 1.5 * player['dbl_dbl'] + 3 * player['trp_dbl']
    return fantasy_pts

midds = playergamelogs.PlayerGameLogs(league_id_nullable = "00",player_id_nullable = 203507, season_nullable = "2021-22", season_type_nullable = "Regular Season" ) 
midds = midds.get_data_frames()[0]
print(dfk_fantasy_pts(midds))

"""
Get Opponent Data (fppg modifier)
"""

"""
Use Machine Learning Models to forecast fppg
"""

"""
push data to sql database
"""

