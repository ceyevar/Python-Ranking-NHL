from django.shortcuts import render
from django.http import HttpResponse, Http404
import numbers, decimal, json, operator, math
from helpers import clustering


###################
# Globals
###################

f = open('./stats.json', 'r')
json_data = f.read()
f.close()

D = json.loads(json_data)

def get_all_players():
    Players = []
    for league in D['Leagues']:
        if league['League Name'] != 'AHL':
            for team in league['Teams']:
                for player in team['Players']:
                    Players.append(player)
    return Players

All_Players = get_all_players()

C = clustering.cluster(All_Players, 10, int(len(All_Players) * 0.047))


###################
# Routes
###################

def index(request):
    return render(request, 'stats/index.html', {'leagues' : D})


def all(request):
    return HttpResponse(json.dumps(D))


def league(request, league_name):
    for league in D["Leagues"]:
        if league["League Name"] == league_name:
            return render(request, 'stats/league.html', {'league' : league})
    raise Http404("League does not exist...")


def player(request, player_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            for player in team["Players"]:
                if player["id"] == int(player_id):
                    Players = collect_players(player['Position'])
                    for k,v in C.iteritems():
                        if player in v:
                            similar_players = v
                    avg = avg_stats(Players)
                    var = variance(Players, avg)
                    dev = deviation(var)
                    player_dev = individual_deviation(player, dev, avg)
                    maxmin = maxmin_stats(Players)
                    return render(request, 'stats/player.html', {'player' : player, 'avg': avg, 'percent': player_dev, 'similar': similar_players })
    raise Http404("League does not exist...")


def team(request, team_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            if team["id"] == int(team_id):
                Teams = get_all_teams()
                avg = avg_stats(Teams)
                var = variance(Teams, avg)
                dev = deviation(var)
                team_dev = individual_deviation(team, dev, avg)
                maxmin = maxmin_stats(Teams)
                percent = percentages(team, maxmin['max'], maxmin['min'])
                return render(request, 'stats/team.html', {'team' : team, 'avg': avg, 'percent': team_dev})
    raise Http404("Team does not exist...")


def compare_players(request, player1_id, player2_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            for player in team["Players"]:
                if player["id"] == int(player1_id):
                    player1 = player
                if player["id"] == int(player2_id):
                    player2 = player


    # If both players are found
    if player1 is not None and player2 is not None:
        return render(request, 'stats/compare_players.html', {'player1': player1, 'player2': player2})
    else:
        raise Http404("One or more players cannot be found...")


def compare_teams(request, team1_id, team2_id):
    data = {}
    data["Teams"] = []
    for league in D["Leagues"]:
        for team in league["Teams"]:
            if team["id"] == int(team1_id) or team["id"] == int(team2_id):
                data["Teams"].append(team)

    # If both teams are found
    if(len(data["Teams"]) == 2):
        return HttpResponse(data["Teams"][0]["Team Name"] + " compared to " + data["Teams"][1]["Team Name"])
    else:
        raise Http404("One or more teams cannot be found...")


##################
# Helper Functions
##################

def avg_stats(data):
    avg = {}
    for item in data:
        for k, v in item.iteritems():
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
    for value in var.values():
        value = math.sqrt(value)
    return var


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


def collect_players(position):
    data = {}
    data['Players'] = []
    for league in D['Leagues']:
        if league['League Name'] != 'AHL':
            for team in league['Teams']:
                for player in team['Players']:
                    if player['Position'] == position:
                        data['Players'].append(player)
    return data['Players']


def get_all_teams():
    Teams = []
    for league in D['Leagues']:
        if league['League Name'] != 'AHL':
            for team in league['Teams']:
                Teams.append(team)
    return Teams