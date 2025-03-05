from django.urls import re_path as url

from spiderweb.views import spiderweb

urlpatterns = [
    url(r'^spiderweb/', spiderweb, name='spiderweb'),
]