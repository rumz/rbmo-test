from django.conf.urls import patterns, include, url
from fund.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^fund_request', fundReleaseForm),
    url(r'^get_budget', getAllocatedBudget),
    url(r'^process_fund_request', processFundRequest),
    url(r'^view_fund_status',  getFundStatus),
    url(r'^view_fstat_detail',  viewFundStatDetails),
)
