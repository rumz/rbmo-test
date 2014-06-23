from django.conf.urls import patterns, include, url
from wfp.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^wfp_form', wfpForm),
    url(r'^wfpinfo', viewWFP),
    url(r'^wfpdetail', getWFPData),
)
