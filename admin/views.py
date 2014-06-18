from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (UserForm, LoginForm, AgencyForm)
from rbmo.models import UserGroup, Groups, Agency, Documents, DocsSubmitted
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import has_permission, get_allowed_tabs
from datetime import datetime


# Create your views here.
SYSTEM_NAME = 'RBMO Management System'

def index(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'form': LoginForm()
    }
    if request.method=='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(password=login_form.cleaned_data['password'], username=login_form.cleaned_data['email'])
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/admin/home/')
            else:
                data['e_msg'] = "Invalid Email or Password"
                return render_to_response('./admin/login.html', data, context)
        else:
            data['frm_errors'] = login_form.errors
            return render_to_response('./admin/login.html', data, context)
    else:
        return render_to_response('./admin/login.html', data, context)


@login_required(login_url='/admin/')
def home(request):
    context = RequestContext(request)
    data = {'page': 'users',
            'system_name': SYSTEM_NAME
        }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    return render_to_response('./admin/home.html', data, context)

def users(request):
    context = RequestContext(request)
    data = { 'page_title': 'Registered Users',
             'system_name': SYSTEM_NAME}
    users = User.objects.all()
    data['users'] = users  
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    return render_to_response('./admin/users.html', data, context)


@login_required(login_url='/admin/')
@transaction.atomic
def addEditUser(request):
    context = RequestContext(request)
    data = {'page_title': 'Add System User',
            'system_name': SYSTEM_NAME,
            'page': 'users',
            'form' : UserForm(),
            'action': request.POST.get('action', 'add')
    }
    if not has_permission(request.user.id, 'add', 'user'):
        return HttpResponseRedirect('/admin/')
        
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if request.method=='POST':
        user_form = UserForm(request.POST)
        #add user
        if data['action']=='add' and user_form.is_valid():
            user = User(email = user_form.cleaned_data['email'],
                        username=  user_form.cleaned_data['email'],
                        first_name = user_form.cleaned_data['first_name'],
                        last_name = user_form.cleaned_data['last_name']
            )
            user.set_password(user.first_name)
            user.save()
            u_group = UserGroup(user = user,
                                group = user_form.cleaned_data['group']
            )
            u_group.save()
            data['s_msg'] = "New User Succesfully saved"
            return render_to_response('./admin/user_form.html', data, context)
        elif data['action']=='edit' and user_form.is_valid():#edit user
            user = User.objects.get(id=request.POST.get('user_id'))
            user.email = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()
            data['s_msg'] = "User Succesfully updated"
            return render_to_response('./admin/user_form.html', data, context)
        else:#invalid form inputs
            data['frm_errors'] = user_form.errors
            data['form'] = user_form
            return render_to_response('./admin/user_form.html', data, context)
    else:
        data['action'] = request.GET.get('action', 'add')
        return render_to_response('./admin/user_form.html', data, context)


@login_required(login_url='/admin/')
def agencies(request):
    context = RequestContext(request)
    data = {'page': 'agencies',
            'system_name': SYSTEM_NAME
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if has_permission(request.user.id, 'add', 'agency'):
        data['has_add'] = 'true'

    if request.method=='POST':
        pass
    else:
        data['agencies'] = Agency.objects.all()
        return render_to_response('./admin/agencies.html', data, context)


@login_required(login_url='/admin/')
def addEditAgency(request):
    context = RequestContext(request)
    data = {'form': AgencyForm(),
            'mode': request.GET.get('mode', 'add'),
            'system_name': SYSTEM_NAME
    }
    if not has_permission(request.user.id, 'add', 'agency'):
        return HttpResponseRedirect('/admin')

    data['allowed_tabs'] = get_allowed_tabs(request.user.id)

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        agency_frm = AgencyForm(request.POST)
        if action=='add' and agency_frm.is_valid():
            addAgency(agency_frm)
            data['s_msg'] = 'New Agency/Office was succesfully added.'
            return render_to_response('./admin/agency_form.html', data, context)
        elif action=='edit' and agency_frm.is_valid():
            pass
        else:
            data['frm_errors'] = agency_frm.errors
            data['form'] = agency_frm
            return render_to_response('./admin/agency_form.html', data, context)
    else:
        return render_to_response('./admin/agency_form.html', data, context)

@login_required(login_url='/admin/')
def agencyMainPage(request):
    context = RequestContext(request)
    cursor  = connection.cursor()
    data = {'agency_id': request.GET.get('agency_id'),
            'system_name': SYSTEM_NAME
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    try:
        agency = Agency.objects.get(id=data['agency_id'])
        docs_subs = Documents.objects.raw('''select * from documents docs
        left join docs_submitted sub_docs on
        docs.id = sub_docs.doc_id and sub_docs.agency_id = %s
        and extract(year from date_submitted) = %s''', [agency.id, 2014])

        cursor.execute("select count(*) as count from docs_submitted where agency_id=%s AND extract(year from date_submitted)=%s", 
                                         [agency.id, 2014]) 

        docs_count = Documents.objects.all().count()
        if docs_count-cursor.fetchone()[0]>0:
            data['remarks'] = 'PENDING'
        else:
            data['remarks'] = 'PROCESSED'
                
        data['agency'] = agency
        data['submitted_docs'] = docs_subs
        return render_to_response('./admin/agency_main_page.html', data, context)
    except Agency.DoesNotExist:
        return render_to_response('./admin/agency_main_page.html', data, context)


@login_required(login_url = '/admin/')
def manageAgencyDocs(request):
    context = RequestContext(request)
    data = {'system_name': SYSTEM_NAME,
            'agency_id' : request.GET.get('agency_id')
    }
    data['allowed_tabs'] = get_allowed_tabs(request.user.id)
    try:
        agency = Agency.objects.get(id=data['agency_id'])
        data['agency'] = agency
        docs_unsubmitted = Documents.objects.raw('''
        SELECT * FROM documents
        WHERE id not in (SELECT doc_id from docs_submitted where agency_id =%s and extract(year from date_submitted)=%s)''',[agency.id, 2014])

        docs_submitted = Documents.objects.raw('''
        select * from documents
        inner join docs_submitted on 
        documents.id = docs_submitted.doc_id and docs_submitted.agency_id=%s
        and extract(year from docs_submitted.date_submitted)=%s
        ''', [agency.id, 2014])

        data['docs_unsubmitted'] = docs_unsubmitted
        data['docs_submitted'] = docs_submitted
        return render_to_response('./admin/agency_docs_recording.html', data, context)
    except Agency.DoesNotExist:
        return render_to_response('./admin/agency_docs_recording.html', data, context)  


@transaction.atomic
def saveSubmitReqs(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        print 'recording'
        agency = Agency.objects.get(id=request.POST.get('agency_id'))
        today = datetime.now()
        for doc in request.POST.getlist('docs[]'):
            document = Documents.objects.get(id=doc)
            doc_submit = DocsSubmitted(agency=agency, doc=document, date_submitted=today.strftime('%Y-%m-%d %I:%M'))
            doc_submit.save()
        return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency.id))

def delSubmitReqs(request):
    docs_sub_id = request.GET.get('doc_sub')
    doc_sub = DocsSubmitted.objects.get(id=docs_sub_id)
    agency_id = doc_sub.agency.id
    doc_sub.delete()
    return HttpResponseRedirect('/admin/manage_agency_docs?agency_id='+str(agency_id))


@transaction.atomic
def addAgency(agency_frm):
    agency = Agency(name = agency_frm.cleaned_data['name'],
                    email = agency_frm.cleaned_data['email'],
                    sector = agency_frm.cleaned_data['sector']
                )
    agency.save()




            
"""
def userGroups(request):
    context = RequestContext(request)
    data = {'page': 'groups',
            'page_title': 'User Groups',
            'system_name': SYSTEM_NAME
        }
    groups = Group.objects.all()
    data['groups'] = groups    
    return render_to_response('./admin/user_groups_main.html', data, context)


def addEditUserGroup(request):
    context = RequestContext(request)
    data = {'permissions': Permission.objects.all(),
            'page' : 'groups',
            'system_name': SYSTEM_NAME,
            'form': GroupForm(),
            'page_title': 'Add User Group and its Permissions',
            'action' : request.POST.get('action', 'add')
    }
    if request.method=='POST':
        grp_frm = GroupForm(request.POST)
        if grp_frm.is_valid() and data['action']=='add':
            group = Group(name = grp_frm.cleaned_data['name'])
            group.save()
            for perm in request.POST.getlist('perms[]'):
                perm_obj = Permission(id=perm)
                group.permissions.add(perm_obj)
            data['s_msg'] = "New User Group Successfully saved"
            return render_to_response('./admin/user_group_form.html', data, context)
        else:
            
            return render_to_response('./admin/user_group_form.html', data, context)            
    else:
        return render_to_response('./admin/user_group_form.html', data, context)
"""