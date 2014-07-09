from django.shortcuts import render, render_to_response, redirect, RequestContext
import time
from django.db import transaction, connection
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import Agency, WFPData, WFPSubmission, PerformanceTarget, CoRequest
from django.contrib.auth.models import User
from .forms import WFPForm, CORequestForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import has_permission, get_allowed_tabs, dictfetchall
from datetime import datetime, date

SYSTEM_NAME = 'RBMO Management System'

months = ['January', 'February', 'March', 'April', 
          'May', 'June', 'July', 'August', 'September', 
          'October', 'November', 'December']

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
            saveWFPData(request, wfp_form, request.POST.get('year'), request.POST.get('agency'))
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
    
@login_required(login_url='/admin/')
@transaction.atomic
def viewWFP(request):
    context = RequestContext(request)
    data = {'system_name'  : SYSTEM_NAME,
            'agency_id'    : request.GET.get('agency_id'),
            'current_year' : time.strftime('%Y'),
            'agency_tab'   : 'wfp'
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    
    if request.method=='POST':
        year = request.POST.get('year')
        agency = Agency.objects.get(id=request.POST.get('agency_id'))
    else:
        year = time.strftime('%Y')
        agency = Agency.objects.get(id=request.GET.get('agency_id'))

    query = '''
    select * from wfp_data
    where allocation=%s and agency_id=%s and year=%s
    '''

    data['year'] = year
    data['agency'] = agency
    try:
        data['wfp_submit'] = WFPSubmission.objects.get(year=year, agency=agency)
    except WFPSubmission.DoesNotExist:
        pass
    
    data['pss'] = WFPData.objects.raw(query, ['PS', agency.id, year])
    data['mooes'] = WFPData.objects.raw(query, ['MOOE', agency.id, year])
    data['cos'] = WFPData.objects.raw(query, ['CO', agency.id, year])
    return render_to_response('./wfp/agency_wfp_info.html', data, context)
    

@transaction.atomic
def getWFPData(request):
    data = {}
    context = RequestContext(request)
    wfp_id = request.GET.get('wfp_id')
    wfp = WFPData.objects.get(id=wfp_id)
    perf_targets = PerformanceTarget.objects.filter(wfp_activity=wfp.id)
    data['wfp'] = wfp
    data['perf_targets'] = perf_targets
    return render_to_response('./wfp/wfp_prog_detail.html', data, context)


'''
helper functions
'''
@transaction.atomic
def saveWFPData(request, wfp_form, year, agency_id):
    wfp = WFPData(
        year = year,
        activity = wfp_form.cleaned_data['activity'],
        allocation = request.POST.get('allocation'),
        agency = Agency.objects.get(id=agency_id),
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
    wfp.total = wfp.jan + wfp.feb + wfp.mar + wfp.apr + wfp.may + wfp.jun + wfp.jul + wfp.aug + wfp.sept + wfp.oct + wfp.nov + wfp.dec

    wfp.save()
    #save performance indicator
    perf_indics = request.POST.getlist('pis[]')
    for pi in perf_indics:
        pi_info = pi.split(';')
        perf_target = PerformanceTarget(wfp_activity=wfp,
                                        indicator=pi_info[0],
                                        q1=pi_info[1],
                                        q2=pi_info[2],
                                        q3=pi_info[3],
                                        q4=pi_info[4]
        )
        perf_target.save()
        


def printWFPData(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME}
    data['agency'] = Agency.objects.get(id=request.GET.get('agency_id'))
    data['year'] = request.GET.get('year') 

    data['wfp_data'] = WFPData.objects.filter(agency=data['agency'], year=data['year'])
    return render_to_response('./wfp/wfp_print.html',data, context)


@login_required(login_url='/admin/')
def viewApprovedBudget(request):
    context = RequestContext(request)
    data = {'system_name'  : SYSTEM_NAME}
    cursor = connection.cursor()
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    try:
        agency = Agency.objects.get(id=request.GET.get('agency_id'))
        data['agency'] = agency
        return render_to_response('./wfp/approved_budget.html', data, context)
    except Agency.DoesNotExist:
        return render_to_response('./wfp/approved_budget.html', data, context)


@login_required(login_url='/admin/')        
def coRequests(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'agency_id'   : request.GET.get('agency_id')}

    try:
        data['allowed_tabs'] = get_allowed_tabs(request.user.id)
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        year = 0
        month = 0
        co_requests = None
        if request.method == 'POST':
            year_month = request.POST.get('month').split('-')
            year = int(year_month[0])
            month = int(year_month[1])
        else:
            year  = int(time.strftime('%Y'))
            month = int(time.strftime('%m'))
            #get current month and year
        co_requests = CoRequest.objects.filter(date_received__year=year, date_received__month=month, agency=agency)
        data['co_requests'] = co_requests
        data['year'] = year
        data['month'] = month
        data['month_str'] = months[month-1]
        
        return render_to_response('./wfp/co_request.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect("/admin/agencies")
    
@login_required(login_url='/admin/')    
def coRequestForm(request):
    context = RequestContext(request)
    data  = {'system_name' : SYSTEM_NAME,
             'agency_id'   : request.GET.get('agency_id'),
             'action'      : request.GET.get('action')
    }
    
    try:
        data['allowed_tabs'] = get_allowed_tabs(request.user.id)
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        
        if request.method == 'POST':
            co_request_form = CORequestForm(request.POST)
            action = request.POST.get('form_action', 'add')
            if action == 'add' and co_request_form.is_valid():
                agency = Agency.objects.get(id=request.POST.get('agency_id'))
                date_rcv = request.POST.get('date_received')
                addCORequest(co_request_form, agency, date_rcv)
                data['s_msg'] = 'New request succesfully Saved'
                data['form']  = CORequestForm()
                return render_to_response('./wfp/co_request_form.html', data, context)
            elif action == 'edit' and co_request_form.is_valid():#edit
                return HttpResponse('edit')
            else:
                return HttpResponse(action)
#        elif request.GET.get()
        else:
            data['form_action'] = request.GET.get('form_action', 'add')
            data['form']   = CORequestForm()
            return render_to_response('./wfp/co_request_form.html', data, context)
    except Agency.DoesNotExist:
        return HttpResponseRedirect("/admin/agencies")

def addCORequest(request_form, agency, date_rcv):
    co_request = CoRequest(date_received = date_rcv,
                          agency = agency,
                          subject = request_form.cleaned_data['subject'],
                          action = request_form.cleaned_data['action'],
                          status = request_form.cleaned_data['status']
                )
    co_request.save()
