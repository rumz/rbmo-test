from django.shortcuts import render, render_to_response, redirect, RequestContext
import time
from django.db import transaction, connection
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import Agency, BudgetAllocation
from django.contrib.auth.models import User
from .forms import WFPForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import has_permission, get_allowed_tabs
from datetime import datetime

SYSTEM_NAME = 'RBMO Management System'

@login_required(login_url='/admin/')
def wfpForm(request):
    context = RequestContext(request)
    data = {'system_name':SYSTEM_NAME,
            'agency_id': request.GET.get('agency_id')
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    data['current_year'] = time.strftime('%Y')
    data['form'] = WFPForm()
    if request.method=='POST':
        wfp_form = WFPForm(request.POST)
        if wfp_form.is_valid():
            saveWFPData(wfp_form, request.POST.get('year'), request.POST.get('agency'))
            data['s_msg'] = 'WFP Entry was succesfully saved'
            data['agency'] = Agency.objects.get(id=request.POST.get('agency'))
            return render_to_response('./wfp/wfp_form.html', data, context)
        else:
            data['frm_errors'] = wfp_form.errors
            data['form'] = wfp_form
            return render_to_response('./wfp/wfp_form.html', data, context)
    else:
        try:
            data['agency'] = Agency.objects.get(id=data['agency_id'])
            return render_to_response('./wfp/wfp_form.html', data, context)
        except Agency.DoesNotExist:
            return HttpResponseRedirect('/admin/agencies')
    

def viewWFP(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'agency_id': request.GET.get('agency_id'),
            'current_year' : time.strftime('%Y')
    }
    
    if request.method=='POST':
        year = request.POST.get('year')
        agency = Agency.objects.get(id=request.POST.get('agency_id'))
    else:
        year = time.strftime('%Y')
        agency = Agency.objects.get(id=request.GET.get('agency_id'))

    query = '''
    select ba.*, a.name from budget_allocation ba inner join
    allocation a on
    ba.allocation_id=a.id and a.name=%s
    where ba.agency_id=%s and year=%s
    '''
    data['year'] = year
    data['agency'] = agency
    data['pss'] = BudgetAllocation.objects.raw(query, ['PS', agency.id, year])
    data['mooes'] = BudgetAllocation.objects.raw(query, ['MOOE', agency.id, year])
    data['cos'] = BudgetAllocation.objects.raw(query, ['CO', agency.id, year])
    return render_to_response('./wfp/agency_wfp_info.html', data, context)
    
    
def getWFPData(request):
    data = {}
    context = RequestContext(request)
    wfp_id = request.GET.get('wfp_id')
    wfp = BudgetAllocation.objects.get(id=wfp_id)
    data['wfp'] = wfp
    return render_to_response('./wfp/wfp_prog_detail.html', data, context)


'''
helper functions
'''
def saveWFPData(wfp_form, year, agency_id):
    budget_alloc = BudgetAllocation(
        year = year,
        activity = wfp_form.cleaned_data['activity'],
        allocation = wfp_form.cleaned_data['allocation'],
        performance_indicator = wfp_form.cleaned_data['performance_indicator'],
        agency = Agency.objects.get(id=agency_id),
        q1 = wfp_form.cleaned_data['q1'],
        q2 = wfp_form.cleaned_data['q2'],
        q3 = wfp_form.cleaned_data['q3'],
        q4 = wfp_form.cleaned_data['q4'],
        jan = wfp_form.cleaned_data['jan'],
        feb = wfp_form.cleaned_data['feb'],
        mar = wfp_form.cleaned_data['mar'],
        apr = wfp_form.cleaned_data['apr'],
        may = wfp_form.cleaned_data['may'],
        jun = wfp_form.cleaned_data['jun'],
        jul = wfp_form.cleaned_data['jul'],
        aug = wfp_form.cleaned_data['aug'],
        sept = wfp_form.cleaned_data['sept'],
        oct = wfp_form.cleaned_data['oct'],
        nov = wfp_form.cleaned_data['nov'],
        dec = wfp_form.cleaned_data['dec']
    )
    budget_alloc.total = budget_alloc.jan + budget_alloc.feb + budget_alloc.mar + budget_alloc.apr + budget_alloc.may + budget_alloc.jun + budget_alloc.jul + budget_alloc.aug + budget_alloc.sept + budget_alloc.oct + budget_alloc.nov + budget_alloc.dec

    budget_alloc.save()
    
    
