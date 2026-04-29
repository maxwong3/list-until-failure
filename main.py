import pandas as pd
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Path
import numpy as np
import unicodedata

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

app.mount("/static", StaticFiles (directory="static"), name="static")

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
    
 
@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/check")
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

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/{page}")
def pages(page: str):
    return FileResponse(f"static/{page}.html")