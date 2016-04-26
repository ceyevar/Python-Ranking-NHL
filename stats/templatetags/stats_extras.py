from django import template
from django.template.defaultfilters import stringfilter
import numbers, math

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
def bartype(avg, value):
	if avg < 1:
		normal = 1
	else:
		normal = avg
	if value > avg + math.log(normal):
		return 'progress-bar-success'
	elif value < avg - math.log(normal):
		return 'progress-bar-danger'
	else:
		return 'progress-bar-warning'


@register.filter()
def comparisoncolors(player1, player2):
	if player1 > player2:
		return 'glyphicon glyphicon-triangle-top green'
	elif player1 < player2:
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