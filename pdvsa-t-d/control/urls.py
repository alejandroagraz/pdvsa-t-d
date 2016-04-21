from django.conf.urls import patterns, url
from control.views import Index, Tables, AddActividad, AddProceso, save_table, Resumen, ExportExcel, ResumenMensual, ExportExcel_anual
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(r'^$', login_required(Index.as_view()), name='index'),
                       url(r'^procesos/(?P<id>[^/]+)/$', login_required(Tables.as_view()), name='tables'),
                       url(r'^save_table/$', save_table, name='save_table'),
                       url(r'^admin/registro/actividades/$', login_required(AddActividad.as_view()), name='add_actividad'),
                       url(r'^admin/registro/procesos/$', login_required(AddProceso.as_view()), name='add_proceso'),
                       url(r'^(?P<tipo>[^/]+)/resumen/(?P<periodo>[^/]+)/$', login_required(Resumen.as_view()), name='resumen'),
                       url(r'^(?P<tipo>[^/]+)/resumen/(?P<periodo>[^/]+)/(?P<mes>[^/]+)/$', login_required(ResumenMensual.as_view()), name='resumen_mensual'),
                       url(r'^(?P<tipo>[^/]+)/resumen/(?P<periodo>[^/]+)/(?P<mes>[^/]+)/Resumen.xlsx/?$', login_required(ExportExcel.as_view()), name='export_excel'),
                       url(r'^(?P<tipo>[^/]+)/resumen/(?P<periodo>[^/]+)/Resumen_anual.xlsx/?$', login_required(ExportExcel_anual.as_view()), name='export_excel_anual'),
                       )
