import sqlite3
import pandas as pd
from pathlib import Path

conn = sqlite3.connect("lahman.db")

csv_dir = Path("lahman_1871-2025_db")

for csv_file in csv_dir.glob("*.csv"):
    table_name = csv_file.stem

    print(f"Importing {table_name}...")

    df = pd.read_csv(csv_file)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

conn.close()

print("Imported db to SQLite.")