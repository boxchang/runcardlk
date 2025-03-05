from django.urls import re_path as url

from spiderweb.views import spiderweb, save_datetime, config_layout, spiderweb_config, abnormal_recover, \
    toggle_device_status

urlpatterns = [
    url(r'^spiderweb/', spiderweb, name='spiderweb'),
    url(r'^save_datetime/', save_datetime, name='save_datetime'),
    url(r'^config/layout', config_layout, name='config_layout'),
    url(r'^config', spiderweb_config, name='spiderweb_config'),
    url(r'^toggle_device_status/', toggle_device_status, name='toggle_device_status'),
    url(r'^abnormal_recover/(?P<pk>\d+)', abnormal_recover, name='abnormal_recover'),
]