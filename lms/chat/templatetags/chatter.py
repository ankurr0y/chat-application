from django import template

register = template.Library()


@register.filter
def slicer(value,arg):
    print(arg)
    return value[:arg]

@register.filter
def adder(value,arg):
    return value+1
