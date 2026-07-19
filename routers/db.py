import sqlite3
conn = sqlite3.connect("lahman.db")
conn.row_factory = sqlite3.Row

cur = conn.execute("""
                   SELECT nameFirst
                   FROM People
                   """)


row = cur.fetchone()

print(row["nameFirst"])