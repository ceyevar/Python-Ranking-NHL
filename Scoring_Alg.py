import json
import re
from stat_collection import import_data


def main():
    import_data()

    f = open('./stats.json', 'r')
    json_data = f.read()

    database = json.loads(json_data)
    stats = ['ES Primary Points/GP', 'ES GF%Rel', 'ES GA']
    stats_n = {}
    for stat_num in stats:
        min_max_vals = normalize(stat_num, database)
        stats_n[stat_num] = min_max_vals

    player_dict = {}
    for index in database['Leagues']:
        for team in index['Teams']:
            for player in team['Players']:
                for stat in player:
                    print ""

def normalize(stat, database):
    min = 0
    max = 0
    min_max = []
    for index in database['Leagues']:
        for team in index['Teams']:
            for player in team['Players']:
                if player[stat] > max:
                    max = player[stat]
                if player[stat] < min:
                    min = player[stat]

    min_max.append(min)
    min_max.append(max)
    return min_max
if __name__ == '__main__':
    main()