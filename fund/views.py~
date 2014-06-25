from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (FundRequestForm)
from rbmo.models import BudgetAllocation, Agency, FundReleases
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import has_permission, get_allowed_tabs, numify
from datetime import datetime
import time

# Create your views here.
SYSTEM_NAME = 'RBMO Management System'

@login_required(login_url='/admin/')
def fundReleaseForm(request):
    context = RequestContext(request)
    data = {'form': FundRequestForm(),
            'system_name' : SYSTEM_NAME,
            'agency_id' : request.GET.get('agency_id'),
            'year' : time.strftime('%Y')
    }
    if data['agency_id'] is None:
        return HttpResponseRedirect('/admin/agencies')
    else:
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        #get all activities for the current year
        activities = BudgetAllocation.objects.filter(agency=data['agency'], year=data['year'])
        data['activities'] = activities

        return render_to_response('./fund/fund_request_form.html', data, context)

@login_required(login_url='/admin/')
def processFundRequest(request):
    context = RequestContext(request)
    data = {'agency_id': request.POST.get('agency_id'),
            'system_name' : SYSTEM_NAME,
            'year' : request.POST.get('year')
    }

    if data['agency_id'] is None:
        return HttpResponseRedirect('/admin/agencies')
    else:
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        #get all activities for the current year
        activities = BudgetAllocation.objects.filter(agency=data['agency'], year=data['year'])
        data['activities'] = activities

    fund_request_form = FundRequestForm(request.POST)
    if fund_request_form.is_valid():
        fund_release = FundReleases(
            budgetallocation = BudgetAllocation.objects.get(id=request.POST.get('activity')),
            month = fund_request_form.cleaned_data['month'],
            date_release = datetime.today(),
            amount = fund_request_form.cleaned_data['amount'],

        )
        fund_release.save()
        
        data['s_msg'] = 'Request Succesfully saved'
        return render_to_response('./fund/fund_request_form.html', data, context)
    else:
        data['frm_errors'] = fund_release.errors
        return render_to_response('./fund/fund_request_form.html', data, context)
    
def getFundStatus(request):
    context = RequestContext(request)
    cursor = connection.cursor()
    releases_query ='''
    select sum(amount) from fund_releases 
    where budgetallocation_id in (select id from budget_allocation where agency_id=%s and year=%s and allocation_id=(select id from allocation where name=%s)) 
    '''
 
    data = {'agency_id' : request.GET.get('agency_id'),
            'year' : request.GET.get('year', time.strftime('%Y'))
    }
    agency = Agency.objects.get(id=data['agency_id'])
    data['agency'] = agency
    # PS
    total_ps = BudgetAllocation.objects.filter(agency=agency, year=data['year'], allocation__name='PS').aggregate(Sum('total'))
    data['total_ps'] = numify(total_ps['total__sum'])
    #MOOE
    total_mooe = BudgetAllocation.objects.filter(agency=agency, year=data['year'], allocation__name='MOOE').aggregate(Sum('total'))
    data['total_mooe'] = numify(total_mooe['total__sum'])
    #CO
    total_co = BudgetAllocation.objects.filter(agency=agency, year=data['year'], allocation__name='CO').aggregate(Sum('total'))
    data['total_co'] = numify(total_co['total__sum'])
    #PS release and balance
    cursor.execute(releases_query, [data['agency_id'], data['year'], 'PS'])
    data['total_ps_release'] = numify(cursor.fetchone()[0])
    data['bal_ps'] = data['total_ps'] - data['total_ps_release']
    #PS release and balance
    cursor.execute(releases_query, [data['agency_id'], data['year'], 'MOOE'])
    data['total_mooe_release'] = numify(cursor.fetchone()[0])
    data['bal_mooe'] = data['total_mooe'] - data['total_mooe_release']
    #PS release and balance
    cursor.execute(releases_query, [data['agency_id'], data['year'], 'CO'])
    data['total_co_release'] = numify(cursor.fetchone()[0])
    data['bal_co'] = data['total_co'] - data['total_co_release']
    
    return render_to_response('./fund/status_of_funds.html', data, context)

def getAllocatedBudget(request):
    cursor = connection.cursor()
    data = {'activity_id': request.GET.get('activity_id'),
            'month' : request.GET.get('month')
    }

    budget = BudgetAllocation.objects.get(id=data['activity_id'])
    cursor.execute('''
    SELECT SUM(amount) FROM fund_releases WHERE budgetallocation_id = %s
    AND month = %s    
    ''', [data['activity_id'], data['month']])

    amount_release = numify(cursor.fetchone()[0])
    amount = 0
    balance = 0
    if data['month'] == '1':
        amount = budget.jan
    elif data['month'] == '2':
        amount = budget.feb
    elif data['month'] == '3':
        amount = budget.mar
    elif data['month'] == '4':
        amount = budget.apr
    elif data['month'] == '5':
        amount = budget.may
    elif data['month'] == '6':
        amount = budget.jun
    elif data['month'] == '7':
        amount = budget.jul
    elif data['month'] == '8':
        amount = budget.aug
    elif data['month'] == '9':
        amount = budget.sept
    elif data['month'] == '10':
        amount = budget.oct
    elif data['month'] == '11':
        amount = budget.nov
    elif data['month'] == '12':
        amount = budget.dec
        
    balance = amount-amount_release
    response = '{"amount": "%s", "balance": "%s"}' %(amount, balance)

    return HttpResponse(response)
    
@login_required(login_url='/admin/')
def viewFundStatDetails(request):
    cursor = connection.cursor()
    context = RequestContext(request)
    data = {'agency_id' : request.GET.get('agency_id'),
            'year'      : request.GET.get('year', time.strftime('%Y')),
            'allocation': request.GET.get('allocation', 'PS')
    }

    releases_query ='''
    select fr.date_release, ba.activity ,fr.amount
    from fund_releases fr inner join budget_allocation ba on 
    fr.budgetallocation_id=ba.id and ba.agency_id=%s and ba.year=%s
    inner join allocation a on
    ba.allocation_id=a.id and a.name=%s
    '''
    
    agency = Agency.objects.get(id = data['agency_id'])
    total_ps = BudgetAllocation.objects.filter(agency = agency, year = data['year'], allocation__name = data['allocation']).aggregate(Sum('total'))
    data['total'] = numify(total_ps['total__sum'])
    temp_total = data['total']
    details = []
    cursor.execute(releases_query, [data['agency_id'], data['year'], data['allocation']])
    for release in cursor.fetchall():
        temp_total = temp_total-release[2]
        details.append({'release_date'   : release[0],
                        'activity'       : release[1],
                        'release_amount' : release[2],
                        'balance'        : temp_total
                    })
    data['fund_stat_details'] = details
        
    return render_to_response('./fund/fund_stat_details.html', data, context)
