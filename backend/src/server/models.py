from django.db import models


# Create your models here.
class secretKeys(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True)
    secretKey = models.CharField(max_length=255)

class Meta:
    db_table = 'secretKey'
    verbose_name = 'Secret Key'
    verbose_name_plural = 'Secret Key'
    ordering = ['user']
