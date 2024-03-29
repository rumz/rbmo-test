from django.conf.urls import patterns, include, url
from .views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^home/$', home),
    url(r'^users/$', users),
    url(r'^add_edit_user/$', addEditUser),
    url(r'^agencies$', agencies),
    url(r'^pm_agency$', addEditAgency),
    url(r'^agency$', agencyMainPage),
    url(r'^manage_agency_docs$',  manageAgencyDocs),
    url(r'^submit_monthly_mpfr$',  submitMPFR),
    url(r'^submit_wfp_req$',  submitWFPReq),
    url(r'^submit_requirements', saveSubmitReqs),
    url(r'^delete_requirement', delSubmitReqs),
    url(r'^monthly_reports$', mpfro),
    url(r'^monthly_reports_form$', mpfro_form),
    url(r'^submit_quarter_reqs$', submitQuarterReq),
    url(r'^allot_releases$', allot_releases),
    url(r'^yearly_fund$', yearly_fund),
    url(r'^yearly_fund?', yearly_fund),
    url(r'^fund_distrib$', fundDistribution),
    url(r'^total_monthly_release$', totalMonthlyReleases)
)
