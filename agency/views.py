from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from .forms import (UserForm, LoginForm, AgencyForm)
from rbmo.models import UserGroup, Groups, Agency
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import has_permission, get_allowed_tabs


SYSTEM_NAME = 'RBMO Management System'




