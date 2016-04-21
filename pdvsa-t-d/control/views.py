from django.views.generic import TemplateView, View
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from control.models import Proceso, ProcesoActividad, Planificacion, Unidad, Actividad
from datetime import datetime
from core.models import Persona
from django.contrib import messages
import json
import xlsxwriter
from xlsxwriter.utility import xl_range_abs


from django.contrib.auth.decorators import login_required


class Index(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


class Tables(TemplateView):
    template_name = "table.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs['id']
        today = datetime.now()
        year = today.strftime("%Y")
        proceso = Proceso.objects.get(id=pk)
        tipo = proceso.tipo
        nombre = proceso.nombre
        actividades = ProcesoActividad.objects.filter(proceso=proceso)
        planificaciones = Planificacion.objects.filter(year=int(year))
        cantidad = actividades.count()
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


@login_required
def save_table(request):
    cont = 0
    # import ipdb; ipdb.set_trace()
    while True:
        if not request.POST.getlist('lista[' + str(cont) + '][id]'):
            break
        idx = int(request.POST.getlist('lista[' + str(cont) + '][id]')[0])
        plan_sap = (request.POST.getlist('lista[' + str(cont) + '][plan_sap]')[0])
        plan_meta = (request.POST.getlist('lista[' + str(cont) + '][plan_meta]')[0])
        real_mc = (request.POST.getlist('lista[' + str(cont) + '][real_mc]')[0])
        plan_hh = (request.POST.getlist('lista[' + str(cont) + '][plan_hh]')[0])
        real_hh = (request.POST.getlist('lista[' + str(cont) + '][real_hh]')[0])
        print 'id: ' + str(idx) + '  pla_sap: ' + plan_sap + ' plan_meta: ' + plan_meta + ' real_mc: ' + real_mc + ' plan_hh:' + plan_hh + ' real_hh:' + real_hh
        Planificacion.objects.filter(id=int(idx)).update(plan_sap=plan_sap,
                                                         plan_meta=plan_meta,
                                                         real_mc=real_mc,
                                                         plan_hh=plan_hh,
                                                         real_hh=real_hh)
        cont = cont + 1
    todo = {"Mensaje": "Registros Guardados"}
    resp = json.dumps(todo, ensure_ascii=False)
    return HttpResponse(resp, content_type='application/json; charset=utf-8')


class AddProceso(TemplateView):
    template_name = "add_proceso.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre', '').upper()
        tipo = request.POST.get('tipo', '').upper()
        descripcion = request.POST.get('descripcion', '')
        if Proceso.objects.filter(nombre=nombre, tipo=tipo):
            messages.info(request, 'El Proceso ' + nombre + ' ya Existe.', 'alert alert-danger')
            form = self.form_class
            return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))
        Proceso(nombre=nombre, tipo=tipo, descripcion=descripcion).save()
        messages.info(request, 'El Proceso ' + nombre + ' fue Registrado con Exito.', 'alert alert-success')
        return HttpResponseRedirect('/control/admin/registro/procesos/')


class AddActividad(TemplateView):
    template_name = "add_actividad.html"

    def get(self, request, *args, **kwargs):
        unidades = Unidad.objects.all()
        procesos = Proceso.objects.all()
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre', '').upper()
        ponderacion = float(request.POST.get('ponderacion', ''))
        id_proceso = int(request.POST.get('proceso', ''))
        id_unidad = int(request.POST.get('unidad', ''))
        if ProcesoActividad.objects.filter(actividad__nombre=nombre, proceso_id=id_proceso):
            unidades = Unidad.objects.all()
            procesos = Proceso.objects.all()
            messages.info(request, 'La Actividad ' + nombre + ' ya Existe en este proceso.', 'alert alert-danger')
            return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))
        proceso = Proceso.objects.get(id=int(id_proceso))
        act = Actividad(nombre=nombre, unidad_id=id_unidad, tipo=proceso.tipo, ponderacion=ponderacion)
        act.save()
        person = Persona.objects.get(user_id=request.user.pk)
        ProcesoActividad(proceso=proceso, actividad=act).save()
        today = datetime.now()
        year = today.strftime("%Y")
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            Planificacion(plan_sap=0,
                          plan_meta=0,
                          real_mc=0,
                          plan_hh=0,
                          real_hh=0,
                          mes=i,
                          year=int(year),
                          actividad=act,
                          persona=person).save()
        messages.info(request, 'La Actividad ' + nombre + ' fue Registrada con Exito.', 'alert alert-success')
        return HttpResponseRedirect('/control/admin/registro/actividades/')


class ResumenMensual(TemplateView):
    template_name = "resumen.html"

    def get(self, request, *args, **kwargs):
        periodo = kwargs['periodo'].upper()
        mes = kwargs['mes']
        print 'mes: ' + mes
        tipo = kwargs['tipo'].upper()
        proces = ProcesoActividad.objects.filter(proceso__tipo=tipo)
        list_actividades = []
        for p in proces:
            dic = {}
            plan_sap = 0
            plan_meta = 0
            real = 0
            plan_hh = 0
            real_hh = 0
            pln = Planificacion.objects.filter(actividad_id=p.actividad.id, mes=mes)
            for pl in pln:
                plan_sap = pl.plan_sap + plan_sap
                plan_meta = pl.plan_meta + plan_meta
                real = pl.real_mc + real
                plan_hh = pl.plan_hh + plan_hh
                real_hh = pl.real_hh + real_hh
            print str(plan_sap / 12)
            dic = {'nombre': p.actividad.nombre,
                   'ponderacion': p.actividad.ponderacion,
                   'unidad': p.actividad.unidad,
                   'plan_sap': str("%.2f" % (((plan_sap / 12) * (real / 12)) / 100)) + '%',
                   'plan_meta': str("%.2f" % (((plan_meta / 12) * (real / 12)) / 100)) + '%',
                   'avance_ponderado': str("%.2f" % (((plan_meta / 12) * (p.actividad.ponderacion)))) + '%',
                   'total_real_hh': str("%.2f" % (((plan_hh / 12) * (real_hh / 12)) / 100)) + '%'}
            list_actividades.append(dic)
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


class Resumen(TemplateView):
    template_name = "resumen.html"

    def get(self, request, *args, **kwargs):
        periodo = kwargs['periodo'].upper()
        tipo = kwargs['tipo'].upper()
        proces = ProcesoActividad.objects.filter(proceso__tipo=tipo)
        list_actividades = []
        for p in proces:
            dic = {}
            plan_sap = 0
            plan_meta = 0
            real = 0
            plan_hh = 0
            real_hh = 0
            pln = Planificacion.objects.filter(actividad_id=p.actividad.id)
            for pl in pln:
                plan_sap = pl.plan_sap + plan_sap
                plan_meta = pl.plan_meta + plan_meta
                real = pl.real_mc + real
                plan_hh = pl.plan_hh + plan_hh
                real_hh = pl.real_hh + real_hh
            print str(plan_sap / 12)
            dic = {'nombre': p.actividad.nombre,
                   'ponderacion': p.actividad.ponderacion,
                   'unidad': p.actividad.unidad,
                   'plan_sap': str("%.2f" % (((plan_sap / 12) * (real / 12)) / 100)) + '%',
                   'plan_meta': str("%.2f" % (((plan_meta / 12) * (real / 12)) / 100)) + '%',
                   'avance_ponderado': str("%.2f" % (((plan_meta / 12) * (p.actividad.ponderacion)))) + '%',
                   'total_real_hh': str("%.2f" % (((plan_hh / 12) * (real_hh / 12)) / 100)) + '%'}
            list_actividades.append(dic)
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


class ExportExcel(View):
    filename = 'filie.xlsx'

    def get(self, request, *args, **kwargs):
        periodo = kwargs['periodo'].upper()
        tipo = kwargs['tipo'].upper()
        mes = kwargs['mes']
        proces = ProcesoActividad.objects.filter(proceso__tipo=tipo)
        list_actividades = []
        print mes + "  mess"
        for p in proces:
            dic = {}
            plan_sap = 0
            plan_meta = 0
            real = 0
            plan_hh = 0
            real_hh = 0
            pln = Planificacion.objects.filter(actividad_id=p.actividad.id, mes=mes)
            for pl in pln:
                plan_sap = pl.plan_sap + plan_sap
                plan_meta = pl.plan_meta + plan_meta
                real = pl.real_mc + real
                plan_hh = pl.plan_hh + plan_hh
                real_hh = pl.real_hh + real_hh
            dic = {'nombre': p.actividad.nombre,
                   'ponderacion': p.actividad.ponderacion,
                   'unidad': p.actividad.unidad,
                   'plan_sap': str("%.2f" % (((plan_sap / 12) * (real / 12)) / 100)) + '%',
                   'plan_meta': str("%.2f" % (((plan_meta / 12) * (real / 12)) / 100)) + '%',
                   'avance_ponderado': str("%.2f" % (((plan_meta / 12) * (p.actividad.ponderacion)))) + '%',
                   'total_real_hh': str("%.2f" % (((plan_hh / 12) * (real_hh / 12)) / 100)) + '%'}
            list_actividades.append(dic)
        wb = xlsxwriter.Workbook(self.filename)
        sheet = wb.add_worksheet('Hoja1')
        section_header_format = wb.add_format({'bold': True,
                                               'align': 'center',
                                               'font_size': 16,
                                               })
        section_subheader_format = wb.add_format({'bold': True,
                                                  'align': 'center',
                                                  'font_size': 13,
                                                  })
        num_format = wb.add_format({'num_format': '0.00%',
                                    'align': 'center',
                                    'font_size': 12,
                                    })
        general_format = wb.add_format({'align': 'center',
                                        'font_size': 12,
                                        })
        sheet.set_column(0, 0, 15, num_format)
        sheet.set_column(1, 1, 50, general_format)
        sheet.set_column(2, 2, 15, general_format)
        sheet.set_column(3, 3, 15, general_format)
        sheet.set_column(4, 4, 15, general_format)
        sheet.set_column(5, 5, 20, general_format)
        sheet.set_column(6, 5, 20, general_format)
        sheet.insert_image(1, 0, 'logo.jpeg')
        sheet.merge_range(0, 0, 0, 6, 'TABLA DE RESUMEN ' + periodo + '(' + tipo + ')', section_header_format)
        row = 1
        sheet.write(row, 0, 'Ponderacion', section_subheader_format)
        sheet.write(row, 1, 'Actividades', section_subheader_format)
        sheet.write(row, 2, 'Unidad', section_subheader_format)
        sheet.write(row, 3, '% Plan Sap', section_subheader_format)
        sheet.write(row, 4, '% Plan Meta', section_subheader_format)
        sheet.write(row, 5, 'Total Real HorasH', section_subheader_format)
        sheet.write(row, 6, 'Avance Ponderado', section_subheader_format)
        print list_actividades
        for x in list_actividades:
            row += 1
            sheet.write(row, 0, ((float(x['ponderacion']) / 100)))
            sheet.write(row, 1, str(x['nombre']))
            sheet.write(row, 2, str(x['unidad']))
            sheet.write(row, 3, str(x['plan_sap']))
            sheet.write(row, 4, str(x['plan_meta']))
            sheet.write(row, 5, str(x['total_real_hh']))
            sheet.write(row, 6, str(x['avance_ponderado']))
        chart = wb.add_chart({'type': 'pie'})
        chart.title_name = 'RESUMEN ' + periodo + '(' + tipo + ')'
        chart.width = sheet._size_col(0) + sheet._size_col(1)
        start_row = 1
        end_row = start_row + list_actividades.__len__() + 1
        values = '=%s!%s' % (sheet.name, xl_range_abs(start_row + 1, 1, end_row - 1, 0))
        categories = '=%s!%s' % (sheet.name, xl_range_abs(start_row + 1, 1, end_row - 1, 1))
        chart.add_series({'values': values, 'categories': categories, 'smooth': True})
        sheet.insert_chart(end_row + 2, 0, chart)
        wb.close()
        return HttpResponse(open(self.filename, 'r').read(), content_type='application/ms-excel')


class ExportExcel_anual(View):
    filename = 'filie.xlsx'

    def get(self, request, *args, **kwargs):
        periodo = kwargs['periodo'].upper()
        tipo = kwargs['tipo'].upper()
        proces = ProcesoActividad.objects.filter(proceso__tipo=tipo)
        list_actividades = []
        for p in proces:
            dic = {}
            plan_sap = 0
            plan_meta = 0
            real = 0
            plan_hh = 0
            real_hh = 0
            pln = Planificacion.objects.filter(actividad_id=p.actividad.id)
            for pl in pln:
                plan_sap = pl.plan_sap + plan_sap
                plan_meta = pl.plan_meta + plan_meta
                real = pl.real_mc + real
                plan_hh = pl.plan_hh + plan_hh
                real_hh = pl.real_hh + real_hh
            dic = {'nombre': p.actividad.nombre,
                   'ponderacion': p.actividad.ponderacion,
                   'unidad': p.actividad.unidad,
                   'plan_sap': str("%.2f" % (((plan_sap / 12) * (real / 12)) / 100)) + '%',
                   'plan_meta': str("%.2f" % (((plan_meta / 12) * (real / 12)) / 100)) + '%',
                   'avance_ponderado': str("%.2f" % (((plan_meta / 12) * (p.actividad.ponderacion)))) + '%',
                   'total_real_hh': str("%.2f" % (((plan_hh / 12) * (real_hh / 12)) / 100)) + '%'}
            list_actividades.append(dic)
        wb = xlsxwriter.Workbook(self.filename)
        sheet = wb.add_worksheet('Hoja1')
        section_header_format = wb.add_format({'bold': True,
                                               'align': 'center',
                                               'font_size': 16,
                                               })
        section_subheader_format = wb.add_format({'bold': True,
                                                  'align': 'center',
                                                  'font_size': 13,
                                                  })
        num_format = wb.add_format({'num_format': '0.00%',
                                    'align': 'center',
                                    'font_size': 12,
                                    })
        general_format = wb.add_format({'align': 'center',
                                        'font_size': 12,
                                        })
        sheet.set_column(0, 0, 15, num_format)
        sheet.set_column(1, 1, 50, general_format)
        sheet.set_column(2, 2, 15, general_format)
        sheet.set_column(3, 3, 15, general_format)
        sheet.set_column(4, 4, 15, general_format)
        sheet.set_column(5, 5, 20, general_format)
        sheet.set_column(6, 5, 20, general_format)
        sheet.insert_image(1, 0, 'logo.jpeg')
        sheet.merge_range(0, 0, 0, 6, 'TABLA DE RESUMEN ' + periodo + '(' + tipo + ')', section_header_format)
        row = 1
        sheet.write(row, 0, 'Ponderacion', section_subheader_format)
        sheet.write(row, 1, 'Actividades', section_subheader_format)
        sheet.write(row, 2, 'Unidad', section_subheader_format)
        sheet.write(row, 3, '% Plan Sap', section_subheader_format)
        sheet.write(row, 4, '% Plan Meta', section_subheader_format)
        sheet.write(row, 5, 'Total Real HorasH', section_subheader_format)
        sheet.write(row, 6, 'Avance Ponderado', section_subheader_format)
        print list_actividades
        for x in list_actividades:
            row += 1
            sheet.write(row, 0, ((float(x['ponderacion']) / 100)))
            sheet.write(row, 1, str(x['nombre']))
            sheet.write(row, 2, str(x['unidad']))
            sheet.write(row, 3, str(x['plan_sap']))
            sheet.write(row, 4, str(x['plan_meta']))
            sheet.write(row, 5, str(x['total_real_hh']))
            sheet.write(row, 6, str(x['avance_ponderado']))
        chart = wb.add_chart({'type': 'pie'})
        chart.title_name = 'RESUMEN ' + periodo + '(' + tipo + ')'
        chart.width = sheet._size_col(0) + sheet._size_col(1)
        start_row = 1
        end_row = start_row + list_actividades.__len__() + 1
        values = '=%s!%s' % (sheet.name, xl_range_abs(start_row + 1, 1, end_row - 1, 0))
        categories = '=%s!%s' % (sheet.name, xl_range_abs(start_row + 1, 1, end_row - 1, 1))
        chart.add_series({'values': values, 'categories': categories, 'smooth': True})
        sheet.insert_chart(end_row + 2, 0, chart)
        wb.close()
        return HttpResponse(open(self.filename, 'r').read(), content_type='application/ms-excel')
