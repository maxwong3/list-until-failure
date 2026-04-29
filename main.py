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

app.mount("/static", StaticFiles (directory="static"), name="static")

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
df = pd.read_csv("lahman_1871-2025_db/People.csv")
df["fullName"] = (df["nameFirst"].fillna("") + " " + df["nameLast"].fillna("")).apply(strip_accents).str.upper()
 
@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/check")
def check (name: str):
    players = df[df["fullName"] == name.upper().strip()]
    if players.empty:
        return {"count": 0, "players": []}
    
    players = players.replace({np.nan: None})

    return {
        "count": len(players),
        "players": players.to_dict(orient="records")
    }

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/{page}")
def pages(page: str):
    return FileResponse(f"static/{page}.html")