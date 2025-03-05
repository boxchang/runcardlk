from django.urls import re_path as url
from runcard.views import barcodepage, search_for_runcard, barcodepage2, runcard_api, thickness_data_api

urlpatterns = [
    url(r'^search', search_for_runcard, name='search'),
    url(r'^barcodepage2/', barcodepage2, name='barcodepage2'),
    url(r'^runcard_api/(?P<runcard>[\w-]+)/$', runcard_api, name='runcard_api'),
    url(r'^thickness_data_api/', thickness_data_api, name='thickness_data_api'),
    url(r'', barcodepage, name='barcodepage'),
]