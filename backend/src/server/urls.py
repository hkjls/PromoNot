from django.urls import path

from .notionFallBack import listenNotionFallback

urlpatterns = [
    path('auth/notion/callback/', listenNotionFallback, name='notion_callback'),
]
