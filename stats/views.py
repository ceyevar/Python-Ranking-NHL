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

C = clustering.cluster(All_Players, 20, int(len(All_Players) * 0.047))

T = { 'Players': [] }

# ids = [1121, 997, 999, 2165, 1555, 1642, 2689, 1015, 1189, 1991, 2003, 1865, 2351, 2211, 1265, 1488, 2121]
# for league in D["Leagues"]:
#     for team in league["Teams"]:
#         for player in team["Players"]:
#             if player["id"] in ids:
#                 T['Players'].append(player)

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


def team_builder(request):
    teamavgs = {}
    avgs = {}
    myavg = {}

    # Calculate my avg
    myk = {}
    for player in T['Players']:
         for k,v in player.iteritems():
            if isinstance(v, numbers.Number) and k != 'id' and k != 'Number':
                if k not in myavg:
                    myk[k] = 0
                    myavg[k] = 0
                myk[k] += 1
                myavg[k] += v
    for k,v in myavg.iteritems():
        myavg[k] = v/myk[k]

    # Calculate team avg for each player stat
    for league in D['Leagues']:
        if league['League Name'] != 'AHL':
            for team in league['Teams']:
                tdata = {}
                tkdata = {}
                for player in team['Players']:
                    for k,v in player.iteritems():
                        if isinstance(v, numbers.Number) and k != 'id' and k != 'Number':
                            if k not in tdata:
                                tkdata[k] = 0
                                tdata[k] = 0
                            tkdata[k] += 1
                            tdata[k] += v
                for k,v in tdata.iteritems():
                    tdata[k] = v/tkdata[k]
                teamavgs[team['id']] = tdata

    # Calculate avg of each stat per team
    kdata = {}
    for team in teamavgs.values():
        for k,v in team.iteritems():
            if k not in avgs:
                kdata[k] = 0
                avgs[k] = 0
            kdata[k] += 1
            avgs[k] += v
    for k,v in avgs.iteritems():
            avgs[k] = v/kdata[k]

    var = variance(teamavgs.values(), avgs)
    dev = deviation(var)
    team_dev = individual_deviation(myavg, dev, avgs)

    if request.is_ajax():
        return render(request, 'stats/_myteam.html', { 'team': T, 'myavg': myavg, 'avgs': avgs, 'percent': team_dev })
    else:
        return render(request, 'stats/myteam.html', { 'team': T, 'myavg': myavg, 'avgs': avgs, 'percent': team_dev })


def add_player(request, playerid):
    for player in All_Players:
        if player['id'] == int(playerid):
            if player not in T['Players']:
                T['Players'].append(player)
                return HttpResponse('Successfully added player to team!')
            else:
                return HttpResponse('Player already exists on team.')
    return HttpResponse('Player not found.')


def remove_player(request, playerid):
    for player in T['Players']:
        if player['id'] == int(playerid):
            T['Players'].remove(player);
            return HttpResponse('Successfully removed player from team!')
    return HttpResponse('Player not found.')


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