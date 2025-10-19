from django.urls import path

from .views import homePage

urlpatterns = [
    path('auth/notion/callback/', homePage, name='home_page'),
]
