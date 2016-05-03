from django.shortcuts import render
from django.http import HttpResponse, Http404
import numbers, decimal, json, operator, math
from helpers import clustering, ranking, helpers


###################
# Globals
###################

f = open('./stats.json', 'r')
json_data = f.read()
f.close()

# All league, team, and player data
D = json.loads(json_data)

# Ignored 'stats' for players
Ignored = ['id', 'Number', 'Draft Year', 'Rank']

# List of all clusters and their players
C = clustering.cluster(helpers.get_all_players(D), 20, 7*3, Ignored)

# Rankings of draft eligible players
# Stat names and weights to collect in ranking algorithm
stats = [{ 'name': 'ES Primary Points/GP', 'weight': .5}, { 'name': 'ES GF%Rel', 'weight': 0.25}, { 'name': 'ES GA', 'weight': 0.25}]
# Player ids in ranking order
Rankings = ranking.rank(helpers.get_draft_elig_players(D), stats, len(helpers.get_draft_elig_players(D)))
Rankings_full = ranking.rank_full_players(helpers.get_draft_elig_players(D), stats, len(helpers.get_draft_elig_players(D)))
# Write rankings to data file
helpers.write_rankings(D, Rankings)

# List of all players in MyTeam
# TODO: store in local cache later
T = { 'Players': [] }

# Used to prepopulate MyTeam for easy demoing
T['Players'] = helpers.populate_myteam(D)

###################
# Routes
###################

def index(request):
    return render(request, 'stats/index.html', {'leagues' : D})


def all(request):
    return HttpResponse(json.dumps(D))
	
def rankings(request, sort):
	return render(request, 'stats/rankings.html', {'rankings' : Rankings_full, 'players': helpers.get_all_players(D), 'sort': sort})
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
                    Players = helpers.collect_players(D, player['Position'])
                    for k,v in C.iteritems():
                        if player in v:
                            similar_players = v
                    avg = helpers.avg_stats(Players, Ignored)
                    var = helpers.variance(Players, avg)
                    dev = helpers.deviation(var)
                    player_dev = helpers.individual_deviation(player, dev, avg)
                    maxmin = helpers.maxmin_stats(Players)
                    return render(request, 'stats/player.html', {'player' : player, 'percent': player_dev, 'similar': similar_players})
    raise Http404("Player does not exist...")


def team(request, team_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            if team["id"] == int(team_id):
                Teams = helpers.get_all_teams(D)
                avg = helpers.avg_stats(Teams, Ignored)
                var = helpers.variance(Teams, avg)
                dev = helpers.deviation(var)
                team_dev = helpers.individual_deviation(team, dev, avg)
                maxmin = helpers.maxmin_stats(Teams)
                percent = helpers.percentages(team, maxmin['max'], maxmin['min'])
                return render(request, 'stats/team.html', {'team' : team, 'percent': team_dev})
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
            if isinstance(v, numbers.Number) and k not in Ignored:
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
                        if isinstance(v, numbers.Number) and k not in Ignored:
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

    var = helpers.variance(teamavgs.values(), avgs)
    dev = helpers.deviation(var)
    team_dev = helpers.individual_deviation(myavg, dev, avgs)

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