from django.shortcuts import render
from django.http import HttpResponse
import json


f = open('./stats.json', 'r')
json_data = f.read()
f.close()

D = json.loads(json_data)

# Create your views here.

def index(request):
    return render(request, 'stats/index.html')

def all(request):
    return HttpResponse(json.dumps(D))

def league(request, league_name):
    for league in D["Leagues"]:
        if league["League Name"] == league_name:
            return render(request, 'stats/league.html', {'league' : league})
    raise Http404("League does not exist...")

# TODO: figure out why this method isn't being routed to

def compare(request, player1, player2):
    print(player1)
    print(player2)
    return HttpResponse("Hello")
