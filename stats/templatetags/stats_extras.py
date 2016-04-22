from django import template
from django.template.defaultfilters import stringfilter
import numbers

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