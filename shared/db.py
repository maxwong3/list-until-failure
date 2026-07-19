import sqlite3
conn = sqlite3.connect("lahman.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

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

def get_player_by_name(name):
    cur = conn.execute("""
                       SELECT * 
                       FROM People
                       WHERE UPPER(nameFirst || ' ' || nameLast) = ?
                       """, (name.upper(),))
    return cur.fetchall()

def get_teams_by_id(player_id):
    cur = conn.execute("""
                       SELECT DISTINCT teamID
                       FROM Appearances
                       WHERE playerID = ?
                       """, (player_id,))
    
    teams = [row["teamID"] for row in cur.fetchall()]

    return {
        teamDict.get(team, team)
        for team in teams
    }

def get_positions_by_id(player_id):
    cur = conn.execute("""
        SELECT
            SUM(G_p) AS G_p,
            SUM(G_c) AS G_c,
            SUM(G_1b) AS G_1b,
            SUM(G_2b) AS G_2b,
            SUM(G_3b) AS G_3b,
            SUM(G_ss) AS G_ss,
            SUM(G_lf) AS G_lf,
            SUM(G_cf) AS G_cf,
            SUM(G_rf) AS G_rf,
            SUM(G_dh) AS G_dh
        FROM Appearances
        WHERE playerID = ?
    """, (player_id,))

    row = cur.fetchone()
    positions = []
    for col, pos in positionDict.items():
        games = row[col]
        if games and games > 0:
            positions.append({"pos": pos, "games": games})

    positions.sort(
        key = lambda x: x["games"],
        reverse=True
    )


    return [p["pos"] for p in positions]