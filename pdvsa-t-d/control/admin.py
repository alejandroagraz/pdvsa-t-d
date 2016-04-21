from django.contrib import admin
from control.models import Actividad, Planificacion, Proceso, ProcesoActividad, Unidad

admin.site.register(Actividad)
admin.site.register(Proceso)
admin.site.register(Planificacion)
admin.site.register(ProcesoActividad)
admin.site.register(Unidad)
