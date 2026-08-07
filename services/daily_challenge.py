from queries.daily_queries import todays_challenge
import unicodedata

def strip_accents(text):
    if not isinstance(text, str):
        return ""
    return "".join([c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)])

def get_daily_challenge():
    challenge = todays_challenge()

    valid_players = []
    valid_ids = set()

    for player in challenge["players"]:
        first = player["nameFirst"] or ""
        last = player["nameLast"] or ""

        full_name = strip_accents(f"{first} {last}").upper().strip()

        valid_players.append(full_name)
        valid_ids.add(player["playerID"])

    challenge["valid_players"] = valid_players
    challenge["valid_ids"] = valid_ids

    return challenge
