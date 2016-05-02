import json
from collections import OrderedDict
from itertools import islice


def rank(players, stats, length):
	player_dict = {}
	stats_n = {}

	for stat_num in stats:
		min_max_vals = normalize(stat_num, players)
		stats_n[stat_num['name']] = min_max_vals


	for player in players:
		if(int(player['GP']) > 40 and int(player['Draft Year']) == 2016):
			player_dict[player['id']] = 0
			stat_dict = {}
			for stat in stats:
					val = (float(player[stat['name']])-float(stats_n[stat['name']][0]))/(float(stats_n[stat['name']][1])-float(stats_n[stat['name']][0]))
					val = val/ find_avg_of_stat(stat['name'], players)
					stat_dict[stat['name']] = val
			player_dict[player['id']] = stat_dict['ES Primary Points/GP'] + 0.5 * stat_dict['ES GF%Rel'] + 0.25 * stat_dict['ES GA']
			for stat in stats:
				player_dict[player['id']] += (stat_dict[stat['name']] * stat['weight'])
	od = OrderedDict(sorted(player_dict.items(), key=lambda t: t[1]))
	player_dict_ordered = OrderedDict(reversed(list(od.items())))

	rakings = list(islice(player_dict_ordered.iteritems(), 0, length))
	results = []
	for player in rakings:
		results.append(player[0])
	return results

def normalize(stat, players):
	min = 0
	max = 0
	min_max = []

	for player in players:
		if player[stat['name']] > max:
			max = player[stat['name']]
		if player[stat['name']] < min:
			min = player[stat['name']]

	min_max.append(min)
	min_max.append(max)
	return min_max


# Returns the average of a given stat for the given league
def find_avg_of_stat(stat_name, players):
	# Set variable
	total_stat = 0
	num_player = 0
	# Iterate players
	for player in players:
		# Find stat for player
		if stat_name in player:
			total_stat += float(player[stat_name])
			num_player += 1
	# Make sure not dividing by 0
	if num_player > 0:
		return total_stat/num_player
	# If the stat isn't present
	else:
		print 'Stat not found for players...'
		return 0
	return 0


if __name__ == '__main__':
	f = open('../../stats.json', 'r')
	D = json.load(f)
	f.close()

	players = []
	stats = [{ 'name': 'ES Primary Points/GP', 'weight': 1}, { 'name': 'ES GF%Rel', 'weight': 0.5}, { 'name': 'ES GA', 'weight': 0.25}]

	for league in D['Leagues']:
		if league['League Name'] != 'AHL':
			for team in league['Teams']:
				for player in team['Players']:
					if int(player['Draft Year']) == 2016:
						players.append(player)

	print rank(players, stats, len(players))