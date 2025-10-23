from django.urls import path

from .views import homePage, webHook

urlpatterns = [
    path('auth/notion/callback/', homePage, name='home_page'),
    path('webhook/notion/', webHook, name='web_hook')
]
