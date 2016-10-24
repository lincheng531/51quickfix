# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response as render
from django.template import RequestContext

def index(request):
    return render('website/index.html', locals(), context_instance=RequestContext(request))

def intro(request):
    return render('website/intro.html', locals(), context_instance=RequestContext(request))