from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.utils.text import slugify
from django.http import HttpResponse
from django.shortcuts import render, redirect
from data.tasks import run_delayed_task, run_task

from .management.commands.gsheetest import Command

def user_main(request):
    return render(request, 'index.html')

def fetch_google_sheet_1(request):
    run_delayed_task.delay('fetchresult_1', -1)
    return redirect('/')

def fetch_google_sheet_2(request):
    run_delayed_task.delay('fetchresult_2', -1)
    return redirect('/')

def fetch_google_sheet_3(request):
    run_delayed_task.delay('fetchresult_3', -1)
    return redirect('/')

def fetch_google_sheet_4(request):
    run_delayed_task.delay('fetchresult_4', -1)
    return redirect('/')

def fetch_google_sheet_5(request):
    run_delayed_task.delay('fetchresult_5', -1)
    return redirect('/')

def reload_google_sheet(request):
    run_delayed_task.delay('fetchdaily', -1)
    return redirect('/')