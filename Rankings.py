from bs4 import BeautifulSoup
import urllib
import json

ranking_dict = {}

r = urllib.urlopen('https://www.nhl.com/news/nhl-central-scoutings-2016-midterm-rankings/c-797902').read()
soup= BeautifulSoup(r, "html.parser")
for row in soup('table')[0].findAll('tr'):
    tds = row('td')[1]
    tds2 = row('td')[0]
    ranking_dict[row('td')[1].string] = tds2.string

print json.dumps(ranking_dict)