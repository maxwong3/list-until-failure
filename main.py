import pandas as pd
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("lahman_1871-2025_db/People.csv")

df["fullName"] = (df["nameFirst"].fillna("") + " " + df["nameLast"].fillna("")).str.upper() 
 
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


app.mount("/static", StaticFiles (directory="static"), name="static")
