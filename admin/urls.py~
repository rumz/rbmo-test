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
    url(r'^submit_requirements', saveSubmitReqs),
    url(r'^delete_requirement', delSubmitReqs),
)
