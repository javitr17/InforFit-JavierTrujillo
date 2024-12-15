from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

class index(TemplateView):
    template_name = 'InForFit/index.html'

