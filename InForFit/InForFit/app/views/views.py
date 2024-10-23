from django.http import HttpResponse
from django.shortcuts import render
from app.forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(login_url='loginAndRegister'), name='dispatch')
class index(View):
    template_name = 'index.html'