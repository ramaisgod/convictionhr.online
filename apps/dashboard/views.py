from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
from django.utils.timezone import now
from datetime import date
from django.db.models import Q
from apps.recruitment.models import *


@login_required
def recruitment_dashboard(request):
    job = Job.objects.all()
    candidate = Candidate.objects.all()
    interview = Interview.objects.all()
    final_select = Candidate.objects.filter(CANDIDATE_STATUS="FINAL SELECT")
    joined = Candidate.objects.filter(CANDIDATE_STATUS="JOINED")
    offered = Candidate.objects.filter(CANDIDATE_STATUS="OFFERED")
    onhold = Candidate.objects.filter(CANDIDATE_STATUS="ON-HOLD")
    dropout = Candidate.objects.filter(CANDIDATE_STATUS="DROP OUT")
    context = {
        'job': job,
        'candidate': candidate,
        'interview': interview,
        'final_select': final_select,
        'joined': joined,
        'offered': offered,
        'onhold': onhold,
        'dropout': dropout,
    }
    return render(request, 'dashboard/recruitment_dashboard.html', context)


@login_required
def my_dashboard(request):
    job = Job.objects.filter(ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username)
    candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_CODE=request.user.username)
    interview = Interview.objects.filter(CREATED_BY=request.user.username)
    final_select = Candidate.objects.filter(CANDIDATE_STATUS="FINAL SELECT", RECRUITER__EMPLOYEE_CODE=request.user.username)
    joined = Candidate.objects.filter(CANDIDATE_STATUS="JOINED", RECRUITER__EMPLOYEE_CODE=request.user.username)
    offered = Candidate.objects.filter(CANDIDATE_STATUS="OFFERED", RECRUITER__EMPLOYEE_CODE=request.user.username)
    onhold = Candidate.objects.filter(CANDIDATE_STATUS="ON-HOLD", RECRUITER__EMPLOYEE_CODE=request.user.username)
    dropout = Candidate.objects.filter(CANDIDATE_STATUS="DROP OUT", RECRUITER__EMPLOYEE_CODE=request.user.username)
    context = {
        'job': job,
        'candidate': candidate,
        'interview': interview,
        'final_select': final_select,
        'joined': joined,
        'offered': offered,
        'onhold': onhold,
        'dropout': dropout,
    }
    return render(request, 'dashboard/my_dashboard.html', context)
