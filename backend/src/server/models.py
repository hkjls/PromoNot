from django.db import models


# Create your models here.
class secretKeys(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.CharField(max_length=255)
    secretKey = models.CharField(max_length=255)

class Meta:
    db_table = 'secretKeys'
    verbose_name = 'Secret Key'
    verbose_name_plural = 'Secret Keys'
    ordering = ['user']

