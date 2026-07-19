from shared.db import conn 

def todays_challenge():
    return get_mets_outfielders()

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

