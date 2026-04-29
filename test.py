import pandas as pd
pd.set_option("display.max_columns", None)

df = pd.read_csv("lahman_1871-2025_db/People.csv")
bat_df = pd.read_csv("lahman_1871-2025_db/Batting.csv")
field_df = pd.read_csv("lahman_1871-2025_db/Fielding.csv")
team_df = pd.read_csv("lahman_1871-2025_db/Teams.csv")
apps_df = pd.read_csv("lahman_1871-2025_db/Appearances.csv")
sal_df = pd.read_csv("lahman_1871-2025_db/Salaries.csv")

print(sal_df[sal_df["teamID"] == "ML4"])