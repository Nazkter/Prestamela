from django import template

###############################################################################
######################## --- CUSTOM FILTER --- ################################
###############################################################################
register = template.Library()

@register.filter(name='iva')
def iva(value):
    return (int(value) * 0.19)
