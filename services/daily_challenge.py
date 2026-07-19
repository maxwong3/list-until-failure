from queries.daily_queries import todays_challenge
import unicodedata

def strip_accents(text):
    if not isinstance(text, str):
        return ""
    return "".join([c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)])

def get_daily_challenge():
    players = todays_challenge()
    valid_players = []
    for player in players:
        first = player["nameFirst"] or ""
        last = player["nameLast"] or ""

        full_name = strip_accents(first + " " + last).upper()

        valid_players.append(full_name)

    return valid_players
