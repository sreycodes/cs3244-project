from django.conf.urls import url
from django.conf import settings
import django.views.static
import webserver.views as views

urlpatterns = [
    url(r'^', views.index, name='index')
]
