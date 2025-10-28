from django.contrib import admin

from .models import WebhookIntegration, secretKeys


# Register your models here.
@admin.register(secretKeys)
class customSecretKeysView(admin.ModelAdmin):
    list_display = (
        'user', 'email'
    )
    search_fields = ('user',)

@admin.register(WebhookIntegration)
class customWebhooIntegration(admin.ModelAdmin):
    list_display = (
        'app_name', 'is_active', 'created_at'
    )
# admin.site.register(secretKeys, customSecretKeysView)