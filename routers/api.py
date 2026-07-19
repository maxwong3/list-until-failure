from fastapi import APIRouter
import pandas as pd
import numpy as np
import unicodedata

from shared.db import get_player_by_name, get_positions_by_id, get_teams_by_id
from services.daily_challenge import get_daily_challenge

 
router = APIRouter()

positionDict = {
    "G_p": "P",
    "G_c": "C",
    "G_1b": "1B",
    "G_2b": "2B",
    "G_3b": "3B",
    "G_ss": "SS",
    "G_lf": "LF",
    "G_cf": "CF",
    "G_rf": "RF",
    "G_dh": "DH"
}

teamDict = {
    "SFN": "SFG",
    "NYA": "NYY",
    "NYN": "NYM",
    "OAK": "ATH",
    "CHN": "CHC", 
    "CHA": "CHW",
    "SDN": "SDP",
    "LAN": "LAD",
    "TBA": "TBR",
    "KCA": "KCR",
    "SLN": "STL"
}

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
df = pd.read_csv("lahman_1871-2025_db/People.csv")
apps_df = pd.read_csv("lahman_1871-2025_db/Appearances.csv")
df["fullName"] = (df["nameFirst"].fillna("") + " " + df["nameLast"].fillna("")).apply(strip_accents).str.upper()

def get_teams(player_id):
    teams = []
    player_df = apps_df[apps_df["playerID"] == player_id]
    for _, row in player_df.iterrows():
        if row["teamID"] not in teams:
            if row["teamID"] in teamDict:
                if teamDict[row["teamID"]] not in teams:
                    teams.append(teamDict[row["teamID"]])
            else:
                teams.append(row["teamID"])
    return teams
def get_positions(player_id):
    player_df = apps_df[apps_df["playerID"] == player_id]
    cols = list(positionDict.keys())
    pos_apps = player_df[cols].sum().sort_values(ascending=False)
    positions = []
    for pos, total in pos_apps.items():
        if total > 0:
            positions.append(positionDict[pos])
    return positions

@router.get("/check")
def check (name: str):
    players = df[df["fullName"] == name.upper().strip()]
    teams = []
    positions = []
    if players.empty:
        return {"count": 0, "players": []}
    
    players = players.replace({np.nan: None})
    for _, row in players.iterrows():
        teams.append(get_teams(row["playerID"]))
        positions.append(get_positions(row["playerID"]))


    return {
        "count": len(players),
        "players": players.to_dict(orient="records"),
        "teams": teams,
        "positions": positions
    }

@router.get("/dailycheck")
def daily_check(name: str):
    name = name.upper().strip()

    valid_players = get_daily_challenge()

    if name not in valid_players:
        return {"count": 0, "players": []}
    
    players = get_player_by_name(name)

    teams = []
    positions = []
    
    for player in players:
        teams.append(get_teams_by_id(player["playerID"]))
        positions.append(get_positions_by_id(player["playerID"]))

    return {
        "count": len(players),
        "players": [dict(player) for player in players],
        "teams": teams,
        "positions": positions
    }

@router.get("/daily")
def get_daily():
    return {
        "message": "daily challenge"
    }