from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.utils.text import slugify
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .management.commands.gsheetest import Command

def user_main(request):
    return render(request, 'index.html')

def fetch_google_sheet_1(request):
    gsheet.handle(gsheet, (), {'type':'fetchresult_1','back_days':-1})
    return redirect('/')

def fetch_google_sheet_2(request):
    gsheet.handle(gsheet, (), {'type':'fetchresult_2','back_days':-1})
    return redirect('/')

def fetch_google_sheet_3(request):
    gsheet.handle(gsheet, (), {'type':'fetchresult_3','back_days':-1})
    return redirect('/')

def fetch_google_sheet_4(request):
    gsheet.handle(gsheet, (), {'type':'fetchresult_4','back_days':-1})
    return redirect('/')

def fetch_google_sheet_5(request):
    gsheet.handle(gsheet, (), {'type':'fetchresult_5','back_days':-1})
    return redirect('/')

def reload_google_sheet(request):
    gsheet = Command()
    gsheet.handle(gsheet, (), {'type':'fetchdaily','back_days':-1})
    return redirect('/')