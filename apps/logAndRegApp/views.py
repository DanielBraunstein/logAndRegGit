# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'logAndRegApp/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Success!")
    return redirect(request, '/success')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.index
    messages.success(request, "Success!")
    return redirect(request, '/success')


def success(request):
    try:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'logAndRegApp/success.html', context)
    except:
        return redirect('/')