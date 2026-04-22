import pandas as pd

df = pd.read_csv("lahman_1871-2025_db/People.csv")
pd.set_option("display.max_columns", None)

print(df[df["nameLast"] == "McGonigle"])