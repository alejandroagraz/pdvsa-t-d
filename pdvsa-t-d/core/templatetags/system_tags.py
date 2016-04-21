from control.models import Proceso
from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def generar_menu(context):
    procesos_transporte = [x for x in Proceso.objects.filter(tipo='TRANSPORTE')]
    procesos_distr = [x for x in Proceso.objects.filter(tipo='DISTRIBUCION')]
    data = []
    data.append('<li class="dropdown">')
    data.append('<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Transporte <span class="caret"></span></a>')
    data.append('<ul class="dropdown-menu">')
    for i in procesos_transporte:
        data.append('<li><a href="/control/procesos/%s">%s</a></li>' % (i.id, i.nombre.lower()))
    data.append('<li role="separator" class="divider"></li>')
    data.append('<li ><a onclick="url_load(this)" data-type="transporte"  data-toggle="modal" href="#modal_mes">Resumen Mensual</a>')
    data.append('<li ><a href="/control/transporte/resumen/anual/">Resumen Anual</a>')
    data.append('</ul>')
    data.append('</li>')

    data.append('<li class="dropdown">')
    data.append('<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Distribucion <span class="caret"></span></a>')
    data.append('<ul class="dropdown-menu" role="menu"> ')
    for i in procesos_distr:
        data.append('<li><a href="/control/procesos/%s">%s</a></li>' % (i.id, i.nombre.lower()))
    data.append('<li role="separator" class="divider"></li>')

    data.append('<li ><a onclick="url_load(this)" data-type="distribucion" data-toggle="modal" href="#modal_mes">Resumen Mensual</a>')
    data.append('<li ><a href="/control/distribucion/resumen/anual/">Resumen Anual</a>')
    data.append('</ul>')
    data.append('</li>')
    return "".join(data)
