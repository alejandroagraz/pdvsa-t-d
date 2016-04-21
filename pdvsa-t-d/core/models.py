from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    cedula = models.IntegerField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '(%s - %s - %s)' % (self.user.first_name, self.user.last_name, self.cedula)

    class Meta:
        db_table = 'personas'
