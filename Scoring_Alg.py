import json
import re
from stat_collection import import_data
from collections import OrderedDict
from helpers import find_avg_of_stat
from itertools import islice
def main():
    import_data()
    player_dict = {}

    f = open('./stats.json', 'r')
    json_data = f.read()

    database = json.loads(json_data)
    del database['Leagues'][0]

    for index in database['Leagues']:
        for team in index['Teams']:
            for player in team['Players']:
                if 'Draft Year' in player:
                    if(int(player['Draft Year']) != 2016):
                        del player

    stats = ['ES Primary Points/GP', 'ES GF%Rel', 'ES GA']
    stats_n = {}
    for stat_num in stats:
        min_max_vals = normalize(stat_num, database)
        stats_n[stat_num] = min_max_vals

    for index in database['Leagues']:
        for team in index['Teams']:
            for player in team['Players']:
                if(int(player['GP']) > 40 and int(player['Draft Year']) == 2016):
                    player_dict[player['Name']] = 0
                    stat_dict = {}
                    for stat in stats:
                            val = (float(player[stat])-float(stats_n[stat][0]))/(float(stats_n[stat][1])-float(stats_n[stat][0]))
                            val = val/ find_avg_of_stat(index['League Name'], stat)
                            stat_dict[stat] = val
                    player_dict[player['Name']] = stat_dict['ES Primary Points/GP'] + 0.5 * stat_dict['ES GF%Rel'] + 0.25 * stat_dict['ES GA']
    od = OrderedDict(sorted(player_dict.items(), key=lambda t: t[1]))
    player_dict_ordered = OrderedDict(reversed(list(od.items())))

    print "Our personal ranking of the 2016 NHL Entry Draft:"

    top_10 = list(islice(player_dict_ordered.iteritems(), 0,9))
    count = 0
    for player in top_10:
        count = count+1
        print str(count) + ". " + str(player[0]) + " (Score: " + str(player[1]) + ")"
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