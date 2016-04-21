from django.shortcuts import render
from django.http import HttpResponse, Http404
import json


f = open('./stats.json', 'r')
json_data = f.read()
f.close()

D = json.loads(json_data)

# Create your views here.

def index(request):
    return render(request, 'stats/index.html', {'leagues' : D})


def all(request):
    return HttpResponse(json.dumps(D))


def league(request, league_name):
    for league in D["Leagues"]:
        if league["League_Name"] == league_name:
            return render(request, 'stats/league.html', {'league' : league})
    raise Http404("League does not exist...")


def player(request, player_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            for player in team["Players"]:
                if player["id"] == int(player_id):
                    return render(request, 'stats/player.html', {'player' : player})
    raise Http404("League does not exist...")


def team(request, team_id):
    for league in D["Leagues"]:
        for team in league["Teams"]:
            if team["id"] == int(team_id):
                return render(request, 'stats/team.html', {'team' : team})
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
        player1_name = data["Players"][0]["Name"]
        player1_name = player1_name.split(',')
        player1_name = player1_name[1] + ' ' + player1_name[0]
        player2_name = data["Players"][1]["Name"]
        player2_name = player2_name.split(',')
        player2_name = player2_name[1] + ' ' + player2_name[0]
        return HttpResponse(player1_name + " compared to " + player2_name)
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
        return HttpResponse(data["Teams"][0]["Team_Name"] + " compared to " + data["Teams"][1]["Team_Name"])
    else:
        raise Http404("One or more teams cannot be found...")
