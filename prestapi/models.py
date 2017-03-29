from django.db import models

# Create your models here.
class Config(models.Model):
    logo            = models.ImageField(null = True, blank = True)
    admin_costs     = models.IntegerField(null = False, default = 16000)
    insurance       = models.IntegerField(null = False, default = 17000)
    system_costs    = models.IntegerField(null = False, default = 24000)
    interest        = models.FloatField(null = False, default = 0.018769)
    iva             = models.FloatField(null = False, default = 0.19)

    class Meta:
        verbose_name_plural = 'Configuraciones'

    def get_iva(self):
        return int((self.admin_costs + self.insurance + self.system_costs) * self.iva)


class Request(models.Model):
    pass

class CreditUser(models.Model):
    first_name      = models.CharField(max_length = 30, default = '')
    last_name       = models.CharField(max_length = 30, default = '')
    fullname        = models.CharField(max_length = 60, default = '')
    gender          = models.CharField(max_length = 1, default = '')
    credit_requests = models.ManyToManyField('Request')

    class Meta:
        verbose_name_plural = 'Usuario de creditos'

    def __str__(self):
        return 'fullname'


class Client(models.Model):
    first_name   = models.CharField(max_length = 30, default = '')
    last_name    = models.CharField(max_length = 30, default = '')
    site_url    = models.CharField(max_length = 300, default = '')
    account_id  = models.IntegerField(null = True, blank = True)
    secret_key  = models.CharField(max_length = 100, default = '')

    class Meta:
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return '{} {} -> [ {} ]'.format(self.first_name, self.last_name, self.site_url)
