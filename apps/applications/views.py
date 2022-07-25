from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.recruitment.models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
from django.utils.timezone import now
from datetime import date, datetime
from django.db.models import Q
from apps.recruitment.functions import getAge
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'layouts/candidate/index.html', context={})


def candidate_profile_upload(request, emp=None):
    obj_emp = get_object_or_404(Employee,  EMPLOYEE_CODE=emp)
    context = {
        'form': OnlineCandidateForm(),
    }
    if request.method == 'POST':
        form = OnlineCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            EMAIL = form.cleaned_data['EMAIL']
            MOBILE_NUMBER = form.cleaned_data['MOBILE_NUMBER']
            SECONDARY_EMAIL = form.cleaned_data['SECONDARY_EMAIL']
            SECONDARY_EMAIL = SECONDARY_EMAIL if SECONDARY_EMAIL else 'None'
            PAN_NUMBER = form.cleaned_data['PAN_NUMBER'].upper()
            # Check if candidate is above 18 years
            DATE_OF_BIRTH = form.cleaned_data['DATE_OF_BIRTH']
            age = getAge(DATE_OF_BIRTH)
            if age < 18 :
                messages.warning(request, "Date of Birth looks invalid. It is below 18 !!!")
                context['form'] = OnlineCandidateForm(request.POST, request.FILES)
                return render(request, 'applications/online_new_candidate.html', context)

            # Check candidate if already exist
            obj_cand = Candidate.objects.filter((Q(PAN_NUMBER=PAN_NUMBER) |
                                                 Q(EMAIL=EMAIL) |
                                                Q(EMAIL=SECONDARY_EMAIL) |
                                                Q(MOBILE_NUMBER=MOBILE_NUMBER) |
                                                Q(SECONDARY_EMAIL=SECONDARY_EMAIL) |
                                                Q(SECONDARY_EMAIL=EMAIL)))
            if len(obj_cand) > 0:
                messages.warning(request, "Profile already exists. Please contact recruiter. !!!")
                context['obj_candidate'] = obj_cand
                context['form'] = OnlineCandidateForm(request.POST, request.FILES)
                return render(request, 'applications/online_new_candidate.html', context)
                # return HttpResponseRedirect(reverse('home'))
            else:
                obj.save()
                id = obj.pk
                obj_candidate = Candidate.objects.get(id=id)
                # Converting to upper case
                obj_candidate.FIRST_NAME = obj_candidate.FIRST_NAME.upper() if obj_candidate.FIRST_NAME else None
                obj_candidate.LAST_NAME = obj_candidate.LAST_NAME.upper() if obj_candidate.LAST_NAME else None
                obj_candidate.LOCATION = obj_candidate.LOCATION.upper() if obj_candidate.LOCATION else None
                obj_candidate.PAN_NUMBER = obj_candidate.PAN_NUMBER.upper() if obj_candidate.PAN_NUMBER else None
                obj_candidate.CANDIDATE_ID = 'CN' + str(id).zfill(4)
                obj_candidate.CANDIDATE_STATUS = "APPLICATION SUBMITTED"
                obj_candidate.CREATED_BY = "SELF"
                obj_candidate.RECRUITER = obj_emp
                obj_candidate.RECRUITER_CODE = emp
                obj_candidate.save()
                context['obj_candidate'] = obj_candidate
                # messages.success(request, f"Your Profile has been created !!! Reference Number is
                # {obj_candidate.CANDIDATE_ID}")
                return render(request, 'applications/thanks.html', context)
        else:
            context['form'] = OnlineCandidateForm(request.POST, request.FILES)
            messages.warning(request, form.errors)
            return render(request, 'applications/online_new_candidate.html', context)
    return render(request, 'applications/online_new_candidate.html', context)


@login_required
def search(request):
    obj_job = Job.objects.filter(Q(ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username) |
                                 Q(ASSIGNED_SPOC__REPORTING_MANAGER_CODE=request.user.username)).distinct().order_by('-TIMESTAMP')
    obj_candidate = Candidate.objects.none()
    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchBy = request.GET.get('SEARCH_BY')
        searchText = request.GET.get('SEARCH_TEXT')
        if searchBy == 'CANDIDATE_ID':
            obj_candidate = Candidate.objects.filter(CANDIDATE_ID=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").order_by('-TIMESTAMP')
        if searchBy == 'CANDIDATE_NAME':
            obj_candidate = Candidate.objects.filter(Q(FIRST_NAME__icontains=searchText) |
                                                     Q(LAST_NAME__icontains=searchText)).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_ID':
            obj_candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_CODE=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_NAME':
            obj_candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_FULL_NAME__icontains=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_CODE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_CODE=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_NAME':
            obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_NAME__icontains=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_CODE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__JOB_CODE=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_TITLE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__JOB_TITLE__icontains=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'PAN_NUMBER':
            obj_candidate = Candidate.objects.filter(PAN_NUMBER=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'MOBILE_NUMBER':
            obj_candidate = Candidate.objects.filter(MOBILE_NUMBER=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'EMAIL':
            obj_candidate = Candidate.objects.filter(EMAIL=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'SOURCE':
            obj_candidate = Candidate.objects.filter(SOURCE=searchText).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if not searchBy:
            obj_candidate = Candidate.objects.filter(Q(CANDIDATE_ID=searchText) |
                                              Q(FIRST_NAME__icontains=searchText) |
                                              Q(LAST_NAME__icontains=searchText) |
                                              Q(RECRUITER__EMPLOYEE_CODE=searchText) |
                                              Q(RECRUITER__EMPLOYEE_FULL_NAME__icontains=searchText) |
                                              Q(JOB_CODE__JOB_CODE=searchText) |
                                              Q(JOB_CODE__JOB_TITLE__icontains=searchText) |
                                              Q(EMAIL=searchText) |
                                              Q(MOBILE_NUMBER=searchText) |
                                              Q(PAN_NUMBER=searchText)).filter(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')

    page = request.GET.get('page', 1)
    paginator = Paginator(obj_candidate, 50)
    try:
        obj_candidate = paginator.page(page)
    except PageNotAnInteger:
        obj_candidate = paginator.page(1)
    except EmptyPage:
        obj_candidate = paginator.page(paginator.num_pages)

    context = {
        'obj_candidate': obj_candidate,
        'obj_job': obj_job,
        'form': SearchApplicationForm(request.GET),
    }
    return render(request, 'applications/search.html', context)


@login_required
def update_job_code(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    if request.method == 'POST':
        JOB_ID = request.POST['JOB_CODE']
        obj_job = Job.objects.get(id=JOB_ID)
        obj_candidate.JOB_CODE = obj_job
        obj_candidate.CANDIDATE_STATUS = "APPROVAL PENDING"
        obj_candidate.save()
        messages.success(request, "Job Code has been assigned !!!")
        return HttpResponseRedirect(reverse(search))


@login_required
def candidate_url(request):
    return render(request, 'applications/candidate_url.html')

