from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.

f = open('./stats.json', 'r')
json_data = f.read()
f.close()

D = json.loads(json_data)

def index(request):
    return HttpResponse("Hello, world. You're at the stats index.")

def all(request):
    return HttpResponse(json.dumps(D))
