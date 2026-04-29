import pandas as pd
pd.set_option("display.max_columns", None)

df = pd.read_csv("lahman_1871-2025_db/People.csv")

print(df[df["retroID"] == "guerv002"])