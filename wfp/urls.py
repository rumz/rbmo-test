from django.conf.urls import patterns, include, url
from wfp.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^wfp_form$', wfpForm),
    url(r'^wfpinfo$', viewWFP),
    url(r'^wfpdetail$', getWFPData),
    url(r'^wfp_print$', printWFPData),
    url(r'^approved_budget$', viewApprovedBudget),
    url(r'^co_request$', coRequests),
    url(r'^co_request_form$', coRequestForm),
)
