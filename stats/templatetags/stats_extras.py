from django import template
from django.template.defaultfilters import stringfilter
import numbers, math, json

register = template.Library()

@register.filter()
@stringfilter
def underscore2space(value):
    return value.replace('_', ' ')


@register.filter()
def get(data, key):
	# Try to fetch from the dict, and if it's not found return an empty string.
	return data.get(key, '')


@register.filter()
def dividedby(numerator, denominator):
	if isnumber(numerator) and isnumber(denominator) and denominator != 0:
  		return numerator/denominator
	else:
		return 0


@register.filter()
def isnumber(value):
	return isinstance(value, numbers.Number)


@register.filter()
def formatname(value):
	value = value.split(',')
	return value[1] + ' ' + value[0]


@register.filter()
def bartype(value):
	if value > 100:
		return 'progress-bar-success progress-bar-striped active'
	elif value > 65:
		return 'progress-bar-success'
	elif value < 35:
		return 'progress-bar-danger'
	else:
		return 'progress-bar-info'


@register.filter()
def comparisoncolors(player1, player2):
	if player1 > player2:
		return 'glyphicon glyphicon-triangle-top green'
	elif player1 < player2:
		return 'glyphicon glyphicon-triangle-bottom red'
	else:
		return 'glyphicon glyphicon-minus yellow'


@register.filter()
def rankcolors(player1, player2):
	if not isinstance(player1, numbers.Number):
		player1 = float('inf')
	if not isinstance(player2, numbers.Number):
		player2 = float('inf')
	if player1 < player2:
		return 'glyphicon glyphicon-triangle-top green'
	elif player1 > player2:
		return 'glyphicon glyphicon-triangle-bottom red'
	else:
		return 'glyphicon glyphicon-minus yellow'


@register.filter()
def comparisonlength(player1, player2):
	try:
		length = float(player1) / (float(player1) + float(player2)) * 100
	except:
		return 50
	else:
		if length > 99:
			length = 99
		elif length < 1:
			length = 1
		return length

@register.filter()
def position(pos):
	switcher = {
        'C': "Center",
		'LW': "Left Winger",
        'RW': "Right Winger",
		'D': "Defenseman",
		'G': "Goaltender",
		'F': "Forward",
		'LD': "Left Defenseman",
		'RD': "Right Defenseman"
    }
	return switcher.get(pos, pos)


@register.filter()
def avgcheck(dev):
	total = 0
	for value in dev.values():
		total += value
	total = total/len(dev)
	if total > 65:
		return 'glyphicon glyphicon-triangle-top green'
	elif total < 35:
		return 'glyphicon glyphicon-triangle-bottom red'
	else:
		return 'glyphicon glyphicon-minus yellow'


@register.assignment_tag
def get_all_data():
	f = open('./stats.json', 'r')
	json_data = f.read()
	f.close()
	return json.loads(json_data)


@register.filter()
def relevant(key):
	return(key not in ['id', 'Number', 'Draft Year'])


@register.filter()
def getrank(player):
	return player.get('Rank', 0)