from shared.db import conn 
from datetime import date

teams = [
    "ARI", "ATL", "BAL", "BOS", "CHN", "CHA", "CIN",
    "CLE", "COL", "DET", "HOU", "KCA", "ANA", "LAN",
    "MIA", "MIL", "MIN", "NYA", "NYN", "OAK", "PHI",
    "PIT", "SDN", "SEA", "SFN", "SLN", "TBA", "TEX",
    "TOR", "WAS"
]

team_names = {
    "ARI": "Diamondbacks",
    "ATL": "Braves",
    "BAL": "Orioles",
    "BOS": "Red Sox",
    "CHN": "Cubs",
    "CHA": "White Sox",
    "CIN": "Reds",
    "CLE": "Guardians",
    "COL": "Rockies",
    "DET": "Tigers",
    "HOU": "Astros",
    "KCA": "Royals",
    "ANA": "Angels",
    "LAN": "Dodgers",
    "MIA": "Marlins",
    "MIL": "Brewers",
    "MIN": "Twins",
    "NYA": "Yankees",
    "NYN": "Mets",
    "OAK": "Athletics",
    "PHI": "Phillies",
    "PIT": "Pirates",
    "SDN": "Padres",
    "SEA": "Mariners",
    "SFN": "Giants",
    "SLN": "Cardinals",
    "TBA": "Rays",
    "TEX": "Rangers",
    "TOR": "Blue Jays",
    "WAS": "Nationals"
}

def example_challenge():
    return get_mets_outfielders()

def todays_challenge():
   index = date.today().toordinal() % len(teams)
   team = teams[index]
   return {
        "title": f"{team_names[team]} Outfielders (Min. 1 Game CF, LF, or RF)",
        "team": team,
        "players": get_outfielders(team)
   }

def get_mets_outfielders():
    cur = conn.execute("""
                    SELECT DISTINCT
                       p.playerID,
                       p.nameFirst,
                       p.nameLast
                    FROM People p
                    JOIN Appearances a
                       ON p.playerID = a.playerID
                    WHERE a.teamID = 'NYN'
                    AND (
                       a.G_lf > 0 OR
                       a.G_cf > 0 OR
                       a.G_rf > 0
                       )


                       """)
    
    return cur.fetchall()

def get_outfielders(team):
    cur = conn.execute(
        """
        SELECT DISTINCT
            p.playerID,
            p.nameFirst,
            p.nameLast
        FROM People p
        JOIN Appearances a
            ON p.playerID = a.playerID
        WHERE a.teamID = ?
        AND (
            a.G_lf > 0 OR
            a.G_cf > 0 OR
            a.G_rf > 0
        )
        """,
        (team,)
    )

    return cur.fetchall()