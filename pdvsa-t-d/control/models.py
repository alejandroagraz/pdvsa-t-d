from django.db import models
from core.models import Persona


class Unidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, null=False, blank=False)

    def __unicode__(self):
        return (self.nombre)

    class Meta:
        db_table = 'unidades'


class Actividad(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    unidad = models.ForeignKey(Unidad)
    tipo = models.CharField(max_length=100)
    ponderacion = models.FloatField()

    def __unicode__(self):
        return (self.nombre)

    class Meta:
        db_table = 'actividades'


class Proceso(models.Model):
    TYPE_CHOICES = (('TRANSPORTE', 'TRANSPORTE'), ('DISTRIBUCION', 'DISTRIBUCION'))
    nombre = models.CharField(max_length=100, null=False, blank=False)
    tipo = models.CharField(max_length=100, choices=TYPE_CHOICES)
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return '(%s - %s)' % (self.nombre, self.tipo)

    class Meta:
        db_table = 'procesos'


class ProcesoActividad(models.Model):
    proceso = models.ForeignKey(Proceso)
    actividad = models.ForeignKey(Actividad)

    def __unicode__(self):
        return '(%s - %s)' % (self.proceso, self.actividad)

    class Meta:
        db_table = 'proceso_actividad'


class Planificacion(models.Model):
    plan_sap = models.FloatField()
    plan_meta = models.FloatField()
    real_mc = models.FloatField()
    plan_hh = models.FloatField()
    real_hh = models.FloatField()
    mes = models.IntegerField()
    year = models.IntegerField()
    actividad = models.ForeignKey(Actividad)
    persona = models.ForeignKey(Persona)

    def __unicode__(self):
        return '(%s - %s ->  mes: %s)' % (self.persona, self.actividad, self.mes)

    class Meta:
        db_table = 'Planificaciones'

    def get_plan_sap(self):
        return str(self.plan_sap).replace(',', '.')

    def get_plan_meta(self):
        return str(self.plan_meta).replace(',', '.')

    def get_real_mc(self):
        return str(self.real_mc).replace(',', '.')

    def get_plan_hh(self):
        return str(self.plan_hh).replace(',', '.')

    def get_real_hh(self):
        return str(self.real_hh).replace(',', '.')
