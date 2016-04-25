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
	if isnumber(numerator) and isnumber(denominator):
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
