from django.shortcuts import render
from django.http import HttpResponse, Http404
import numbers, decimal, json, operator


f = open('./stats.json', 'r')
json_data = f.read()
f.close()

D = json.loads(json_data)


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
                    avg = local_avg_stats(team, 'Players')
                    maxmin = local_maxmin_stats(team, 'Players')
                    percent = percentages(player, maxmin['max'], maxmin['min'])
                    return render(request, 'stats/player.html', {'player' : player, 'avg': avg, 'percent': percent, 'maxmin': maxmin, 'teammates':team['Players'] })
    raise Http404("League does not exist...")


def team(request, team_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            if team["id"] == int(team_id):
                avg = local_avg_stats(league, 'Teams')
                maxmin = local_maxmin_stats(league, 'Teams')
                percent = percentages(team, maxmin['max'], maxmin['min'])
                return render(request, 'stats/team.html', {'team' : team, 'avg': avg, 'percent': percent, 'maxmin': maxmin})
    raise Http404("League does not exist...")


def compare_players(request, player1_id, player2_id):
    data = {}
    data["Players"] = []
    for league in D["Leagues"]:
        for team in league["Teams"]:
            for player in team["Players"]:
                if player["id"] == int(player1_id) or player["id"] == int(player2_id):
                    data["Players"].append(player)

    # If both players are found
    if(len(data["Players"]) == 2):
        return render(request, 'stats/compare_players.html', {'player1': data['Players'][0], 'player2': data['Players'][1]})
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

def local_avg_stats(data, datatype):
    avg = {}
    for item in data[datatype]:
        for k, v in item.iteritems():
            if k in avg:
                if isinstance(v, numbers.Number):
                    avg[k] += v
            else:
                if isinstance(v, numbers.Number):
                    avg[k] = v
    for k, v in avg.iteritems():
        avg[k] = v/len(data[datatype])
    return avg


def local_maxmin_stats(data, datatype):
    max = {}
    min = {}
    for item in data[datatype]:
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