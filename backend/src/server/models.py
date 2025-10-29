from django.db import models


# Create your models here.
class secretKeys(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True)
    secretKey = models.CharField(max_length=255)
    notion_bot_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    notion_workspace_id = models.CharField(max_length=255, null=True, blank=True)

class Meta:
    db_table = 'secretKey'
    verbose_name = 'Secret Key'
    verbose_name_plural = 'Secret Key'
    ordering = ['user']


class WebhookIntegration(models.Model):
    app_name = models.CharField(max_length=100, help_text="Le nom de l'application")
    verification_token = models.CharField(max_length=255, blank=True, null=True,
                                          help_text='Le token de verification recu')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.app_name

    class Meta:
        verbose_name = "Integration Webhook"
        verbose_name_plural = "Integration Webhook"
