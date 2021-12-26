# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 01:52:57 2021

@author: thyang
"""

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs
import pandas as pd

active_players = players.get_active_players()
all_players_box_score = pd.DataFrame()
for player in active_players:
    player_id = player['id']
    player_box_score = playergamelogs.PlayerGameLogs(league_id_nullable = "00",player_id_nullable = player_id, season_nullable = "2021-22", season_type_nullable = "Regular Season" )
    player_box_score = player_box_score.get_data_frames()[0]
    all_players_box_score = all_players_box_score.append(player_box_score)