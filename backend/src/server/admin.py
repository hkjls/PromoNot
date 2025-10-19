from django.contrib import admin

from .models import secretKeys


# Register your models here.
@admin.register(secretKeys)
class customSecretKeysView(admin.ModelAdmin):
    list_display = (
        'user', 'email'
    )
    search_fields = ('user',)

# admin.site.register(secretKeys, customSecretKeysView)