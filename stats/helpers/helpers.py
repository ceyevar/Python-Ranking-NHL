import numbers, decimal, json, operator, math


##################
# Helper Functions
##################

def get_draft_elig_players(D):
	players = []
	for league in D['Leagues']:
		if league['League Name'] != 'AHL':
			for team in league['Teams']:
				for player in team['Players']:
					if int(player['Draft Year']) == 2016:
						players.append(player)
	return players


def get_all_players(D):
	Players = []
	for league in D['Leagues']:
		if league['League Name'] != 'AHL':
			for team in league['Teams']:
				for player in team['Players']:
					Players.append(player)
	return Players

def populate_myteam(D):
	players = []
	ids = [1121, 997, 999, 2165, 1555, 1642, 2689, 1015, 1189, 1991, 2003, 1865, 2351, 2211, 1265, 1488, 2121]
	for league in D["Leagues"]:
		for team in league["Teams"]:
			for player in team["Players"]:
				if player["id"] in ids:
					players.append(player)
	return players


def avg_stats(data, ignored):
    avg = {}
    for item in data:
        for k, v in item.iteritems():
            if k not in ignored:
                if k in avg:
                    if isinstance(v, numbers.Number):
                        avg[k] += v
                else:
                    if isinstance(v, numbers.Number):
                        avg[k] = v
    for k, v in avg.iteritems():
        avg[k] = v/len(data)
    return avg


def variance(data, avg):
    var = {}
    for k,v in avg.iteritems():
        for item in data:
            if k in item:
                if k not in var:
                    var[k] = 0
                var[k] += (item[k] - v) ** 2
        if k in var:
            var[k] = var[k]/len(data)
    return var


def deviation(var):
    dev = {}
    for k,v in var.iteritems():
        dev[k] = math.sqrt(v)
    return dev


def individual_deviation(data, dev, avg):
    pd = {}
    for k,v in dev.iteritems():
        if k in data:
            numerator = (float(data[k]) - float(avg[k] - v))
            denominator = (float(avg[k] + v) - float(avg[k] - v))
            try:
                pd[k] = ((numerator/denominator) * 100)
            except:
                pd[k] = 50
            else:
                if pd[k] == 0:
                    pd[k] = 1
    return pd


def maxmin_stats(data):
    max = {}
    min = {}
    for item in data:
        for k,v in item.iteritems():
            if k in max and k in min:
                if isinstance(v, numbers.Number):
                    if max[k] < v:
                        max[k] = v
                    if min[k] > v:
                        min[k] = v
            else:
                if isinstance(v, numbers.Number):
                    max[k] = v
                    min[k] = v
    return { 'max': max, 'min': min }


def percentages(data, max, min):
    result = {}
    for k,v in data.iteritems():
        if isinstance(v, numbers.Number):
            numerator = (float(v) - float(min[k]))
            denominator = (float(max[k]) - float(min[k]))
            try:
                result[k] = ((numerator/denominator) * 100)
            except:
                result[k] = 100
    return result


def collect_players(D, position):
    data = {}
    data['Players'] = []
    for league in D['Leagues']:
        if league['League Name'] != 'AHL':
            for team in league['Teams']:
                for player in team['Players']:
                    if player['Position'] == position:
                        data['Players'].append(player)
    return data['Players']


def get_all_teams(D):
    Teams = []
    for league in D['Leagues']:
        if league['League Name'] != 'AHL':
            for team in league['Teams']:
                Teams.append(team)
    return Teams


def write_rankings(D, rankings):
	for league in D['Leagues']:
		if league['League Name'] != 'AHL':
			for team in league['Teams']:
				for player in team['Players']:
					if player['id'] in rankings:
						player['Rank'] = (rankings.index(player['id']) + 1)