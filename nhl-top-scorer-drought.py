import requests
import csv
import json
import argparse
import os
from datetime import date



def get_players_sorted(season):
    url = f"https://api.nhle.com/stats/rest/en/skater/summary?cayenneExp=seasonId={season} and gameTypeId=2&limit=-1"
    data = requests.get(url).json()

    # Sort by goals scored (you may need to rearrange depending on API response)
    players = data["data"]
    players = sorted(players, key=lambda p: p["goals"], reverse=True)
    
    return players


def evaluate_goal_scorer(player_id, drought_game_threshold):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    data = requests.get(url).json()

    data['isDue'] = True

    last5Game = data['last5Games']
    for i in range(0,drought_game_threshold):
        if last5Game[i]['goals'] > 0:
            data['isDue'] = False
            
    return data

        

def main(season, drought_threshold, playerCheckLimit):

    today = date.today()
    formattedDate = today.strftime("%Y-%m-%d")  # "2025-11-06"
    path = f"results/season/{season}/{formattedDate}"
    os.makedirs(path, exist_ok=True)  # create folder if it doesn't exist

    print("gathering list of NHL players sorted by goals...")
    players = get_players_sorted(season)
    limit = playerCheckLimit
    limitCount = 0

    data = []
    playerStatsJsonDue = []
    playerStatsSanityCheck = []
    print(f"evaluating top {playerCheckLimit} players in season {season} based on goal drought threshold ({drought_threshold}) from most recent games...")
    for player in players:
       
        if limitCount >= limit:
            break

        player = evaluate_goal_scorer(player['playerId'], drought_threshold)

        last5GamesNormalized = []

        for game in player['last5Games']:
            last5GamesNormalized.append({"gameDate": game['gameDate'],
                                        "goals":game['goals'],
                                        "oppenent":game['opponentAbbrev']})

        if player['isDue']:
            print(player['firstName']['default'] + " " + player['lastName']['default'] + " is due")
            data.append({"player name": player['firstName']['default'] + " " + player['lastName']['default']})


            playerStatsJsonDue.append({"playerId":player['playerId'],
                                    "fullName":player['firstName']['default'] + " " + player['lastName']['default'],
                                    "team":player['currentTeamAbbrev'],
                                    "isCurrentlyActive":player['isActive'],
                                    "goals20252026":player['featuredStats']['regularSeason']['subSeason']['goals'],
                                    "last5Games":last5GamesNormalized
                                    })
        
        playerStatsSanityCheck.append({"playerId":player['playerId'],
                                    "fullName":player['firstName']['default'] + " " + player['lastName']['default'],
                                    "team":player['currentTeamAbbrev'],
                                    "isCurrentlyActive":player['isActive'],
                                    "goals20252026":player['featuredStats']['regularSeason']['subSeason']['goals'],
                                    "last5Games":last5GamesNormalized
                                    })
        
        limitCount += 1




    with open(f"{path}/players_due.json", "w") as f:
                json.dump(playerStatsJsonDue, f, indent=4)    
    
    with open(f"{path}/players_sanity_check.json", "w") as f:
                json.dump(playerStatsSanityCheck, f, indent=4)   

    with open(f"{path}/name_output.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["player name"])
        writer.writeheader()
        writer.writerows(data)

    print(f"finished evaluation: {len(data)} of the top {playerCheckLimit} goal scorers in season {season} are currently detected to be in a {drought_threshold} game goal drought")


# -----------------------------
# CLI argument parser
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NHL Goal Drought Checker")
    parser.add_argument(
        "--season", type=int, default=2,
        help="Season to evaluate from"
    )
    parser.add_argument(
        "--dt", type=int, default=2,
        help="Number of consecutive games without a goal to count as a drought"
    )
    parser.add_argument(
        "--playerLimit", type=int, default=50,
        help="Maximum number of top scorers to check"
    )

    args = parser.parse_args()

    main(season=args.season,drought_threshold=args.dt, playerCheckLimit=args.playerLimit)
