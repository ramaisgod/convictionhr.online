from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
from django.utils.timezone import now
from datetime import date, datetime
from django.db.models import Q
from .functions import getAge


@login_required
def create_job(request):
    context = {
        'form': JobForm(),
    }
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            START_DATE = form.cleaned_data['JOB_START_DATE']
            TARGET_DATE = form.cleaned_data['TARGET_DATE']
            if TARGET_DATE < START_DATE:
                context['form'] = JobForm(request.POST)
                messages.warning(request, "Target Date must be greater than Job Start Date")
                return render(request, 'recruitment/create_job.html', context)
            form.save()
            obj = form.save(commit=False)
            obj.save()
            id = obj.pk
            context['id'] = id
            obj_job = Job.objects.get(id=id)
            # Converting to upper case
            # obj_client.PAN_NUMBER = obj_client.PAN_NUMBER.upper() if obj_client.PAN_NUMBER else None
            # obj_client.GSTIN_NUMBER = obj_client.GSTIN_NUMBER.upper() if obj_client.GSTIN_NUMBER else None
            obj_job.JOB_CODE = 'J' + str(id).zfill(3)
            obj_job.JOB_OPENING_STATUS = "IN-PROGRESS"
            obj_job.CREATED_BY = request.user.username
            obj_job.save()
            obj_job = Job.objects.get(id=id)
            context['form'] = JobForm(instance=obj_job)
            context['obj_job'] = obj_job
            context['activeTab_No'] = 1
            messages.success(request, f"Job has been created !!! Job Code is {obj_job.JOB_CODE}")
            # return render(request, 'recruitment/create_details.html', context)
            # return HttpResponseRedirect(f'/recruitment/job/{id}/details/')
            return HttpResponseRedirect(reverse(job_list))
        else:
            context['form'] = JobForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'recruitment/create_job.html', context)
    return render(request, 'recruitment/create_job.html', context)


@login_required
def clone_job(request, id=None):
    obj_job = Job.objects.get(id=id)
    context = {
        'form': JobForm(instance=obj_job),
        'obj_job': obj_job,
    }
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            # form.save()
            START_DATE = form.cleaned_data['JOB_START_DATE']
            TARGET_DATE = form.cleaned_data['TARGET_DATE']
            if TARGET_DATE < START_DATE:
                context['form'] = JobForm(request.POST)
                messages.warning(request, "Target Date must be greater than Job Start Date")
                return render(request, 'recruitment/clone_job.html', context)
            obj = form.save(commit=False)
            obj.pk = None
            obj.save()
            id = obj.pk
            context['id'] = id
            obj_job = Job.objects.get(id=id)
            obj_job.JOB_CODE = 'J' + str(id).zfill(3)
            obj_job.JOB_OPENING_STATUS = "IN-PROGRESS"
            obj_job.CREATED_BY = request.user.username
            obj_job.MODIFIED_BY = ''
            obj_job.LAST_MODIFIED = None
            obj_job.save()
            obj_job = Job.objects.get(id=id)
            context['form'] = JobForm(instance=obj_job)
            context['obj_job'] = obj_job
            context['activeTab_No'] = 1
            messages.success(request, f"Job has been created !!! Job Code is {obj_job.JOB_CODE}")
            # return HttpResponseRedirect(f'/recruitment/job/{obj_job.id}/details/')
            return HttpResponseRedirect(reverse(job_list))
        else:
            context['form'] = JobForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'recruitment/clone_job.html', context)
    return render(request, 'recruitment/clone_job.html', context)


@login_required
def job_details(request, id=None):
    obj_job = Job.objects.get(id=id)
    context = {
        'form': JobForm(instance=obj_job),
        'obj_job': obj_job,
    }
    if request.method == 'POST':
        form = JobForm(request.POST, instance=obj_job)
        if form.is_valid():
            START_DATE = form.cleaned_data['JOB_START_DATE']
            TARGET_DATE = form.cleaned_data['TARGET_DATE']
            if TARGET_DATE < START_DATE:
                context['form'] = JobForm(request.POST)
                messages.warning(request, "Target Date must be greater than Job Start Date")
                return render(request, 'recruitment/create_job.html', context)
            form.save()
            obj_job = Job.objects.get(id=id)
            obj_job.MODIFIED_BY = request.user.username
            obj_job.LAST_MODIFIED = now()
            obj_job.save()
            # Converting to upper case
            # obj_client.PAN_NUMBER = obj_client.PAN_NUMBER.upper() if obj_client.PAN_NUMBER else None
            # obj_client.GSTIN_NUMBER = obj_client.GSTIN_NUMBER.upper() if obj_client.GSTIN_NUMBER else None
            # obj_job.save()
            context['form'] = JobForm(instance=obj_job)
            messages.success(request, "Data has been updated !!!")
            # return render(request, 'recruitment/job_details.html', context)
            return HttpResponseRedirect(reverse(job_list))
        else:
            context['form'] = JobForm(request.POST, instance=obj_job)
            messages.warning(request, form.errors)
            return render(request, 'recruitment/job_details.html', context)
    return render(request, 'recruitment/job_details.html', context)


@login_required
def job_list(request):
    obj_job = Job.objects.all().order_by('-TIMESTAMP')
    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchBy = request.GET.get('SEARCH_BY')
        searchText = request.GET.get('SEARCH_TEXT')
        if searchBy == 'JOB_CODE':
            obj_job = Job.objects.filter(JOB_CODE=searchText).order_by('-TIMESTAMP')
        if searchBy == 'JOB_TITLE':
            obj_job = Job.objects.filter(JOB_TITLE__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_ID':
            obj_job = Job.objects.filter(ASSIGNED_SPOC__EMPLOYEE_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_NAME':
            obj_job = Job.objects.filter(Q(ASSIGNED_SPOC__FIRST_NAME__icontains=searchText) |
                                         Q(ASSIGNED_SPOC__MIDDLE_NAME__icontains=searchText) |
                                         Q(ASSIGNED_SPOC__LAST_NAME__icontains=searchText)).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CLIENT_CODE':
            obj_job = Job.objects.filter(CLIENT_CODE__CUSTOMER_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CLIENT_NAME':
            obj_job = Job.objects.filter(CLIENT_CODE__CUSTOMER_NAME__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_DESCRIPTION':
            obj_job = Job.objects.filter(JOB_DESCRIPTION__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'REQUIRED_SKILLS':
            obj_job = Job.objects.filter(REQUIRED_SKILLS__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CREATED_BY':
            obj_job = Job.objects.filter(CREATED_BY=searchText).distinct().order_by('-TIMESTAMP')
        if not searchBy:
            obj_job = Job.objects.filter(Q(JOB_CODE=searchText) |
                                         Q(ASSIGNED_SPOC__EMPLOYEE_CODE=searchText) |
                                              Q(JOB_TITLE__icontains=searchText) |
                                              Q(CLIENT_CODE__CUSTOMER_CODE=searchText) |
                                              Q(CLIENT_CODE__CUSTOMER_NAME__icontains=searchText) |
                                              Q(JOB_DESCRIPTION__icontains=searchText) |
                                              Q(REQUIRED_SKILLS__icontains=searchText)).distinct().order_by('-TIMESTAMP')

    page = request.GET.get('page', 1)
    paginator = Paginator(obj_job, 50)
    try:
        obj_job = paginator.page(page)
    except PageNotAnInteger:
        obj_job = paginator.page(1)
    except EmptyPage:
        obj_job = paginator.page(paginator.num_pages)
    return render(request, 'recruitment/job_list.html', {'obj_job': obj_job, 'form': SearchJobForm(request.GET)})


@login_required
def assigned_job(request):
    obj_job = Job.objects.filter(ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).order_by('-TIMESTAMP')
    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchBy = request.GET.get('SEARCH_BY')
        searchText = request.GET.get('SEARCH_TEXT')
        if searchBy == 'JOB_CODE':
            obj_job = Job.objects.filter(JOB_CODE=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).order_by('-TIMESTAMP')
        if searchBy == 'JOB_TITLE':
            obj_job = Job.objects.filter(JOB_TITLE__icontains=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CLIENT_CODE':
            obj_job = Job.objects.filter(CLIENT_CODE__CUSTOMER_CODE=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CLIENT_NAME':
            obj_job = Job.objects.filter(CLIENT_CODE__CUSTOMER_NAME__icontains=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_DESCRIPTION':
            obj_job = Job.objects.filter(JOB_DESCRIPTION__icontains=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
        if searchBy == 'REQUIRED_SKILLS':
            obj_job = Job.objects.filter(REQUIRED_SKILLS__icontains=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
        if searchBy == 'ASSIGNED_BY':
            obj_job = Job.objects.filter(CREATED_BY=searchText, ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
        if not searchBy:
            obj_job = Job.objects.filter(Q(JOB_CODE=searchText) |
                                         Q(CREATED_BY=searchText) |
                                              Q(JOB_TITLE__icontains=searchText) |
                                              Q(CLIENT_CODE__CUSTOMER_CODE=searchText) |
                                              Q(CLIENT_CODE__CUSTOMER_NAME__icontains=searchText) |
                                              Q(JOB_DESCRIPTION__icontains=searchText) |
                                              Q(REQUIRED_SKILLS__icontains=searchText), ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).distinct().order_by('-TIMESTAMP')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_job, 50)
    try:
        obj_job = paginator.page(page)
    except PageNotAnInteger:
        obj_job = paginator.page(1)
    except EmptyPage:
        obj_job = paginator.page(paginator.num_pages)
    return render(request, 'recruitment/assigned_job.html', {'obj_job': obj_job, 'form': SearchAssignedJobForm(request.GET)})


@login_required
def new_candidate(request):
    obj_job = Job.objects.filter(Q(ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username) |
                                 Q(ASSIGNED_SPOC__REPORTING_MANAGER_CODE=request.user.username)).distinct().order_by('-TIMESTAMP')
    context = {
        'form': NewCandidateForm(),
        'obj_job': obj_job,
    }
    if request.method == 'POST':
        print(request.POST)
        form = NewCandidateForm(request.POST, request.FILES)
        intStatus = request.POST.get('intStatus')
        job_code = request.POST.get('JOB_CODE')
        print(intStatus)
        print(job_code)
        if (intStatus == 'Interested') and (not job_code):
            messages.warning(request, "Please select a Job Code")
            context['form'] = NewCandidateForm(request.POST, request.FILES)
            return render(request, 'recruitment/new_candidate.html', context)
        if form.is_valid():
            obj = form.save(commit=False)
            EMAIL = form.cleaned_data['EMAIL']
            MOBILE_NUMBER = form.cleaned_data['MOBILE_NUMBER']
            SECONDARY_EMAIL = form.cleaned_data['SECONDARY_EMAIL']
            SECONDARY_EMAIL = SECONDARY_EMAIL if SECONDARY_EMAIL else 'None'
            JOB_CODE = form.cleaned_data['JOB_CODE']
            PAN_NUMBER = form.cleaned_data['PAN_NUMBER'].upper()
            # Check if Job TARGET DATE is expired
            if intStatus == 'Interested':
                if JOB_CODE.TARGET_DATE < date.today():
                    messages.warning(request, f"Job Code {JOB_CODE.JOB_CODE} is expired. please contact HR Manager !!!")
                    context['form'] = NewCandidateForm(request.POST, request.FILES)
                    return render(request, 'recruitment/new_candidate.html', context)

            # Check if candidate is above 18 years
            DATE_OF_BIRTH = form.cleaned_data['DATE_OF_BIRTH']
            age = getAge(DATE_OF_BIRTH)
            if age < 18 :
                messages.warning(request, "Date of Birth looks invalid. It is below 18 !!!")
                context['form'] = NewCandidateForm(request.POST, request.FILES)
                return render(request, 'recruitment/new_candidate.html', context)

            # Check candidate if already exist
            obj_cand = Candidate.objects.filter((Q(PAN_NUMBER=PAN_NUMBER) |
                                                 Q(EMAIL=EMAIL) |
                                                Q(EMAIL=SECONDARY_EMAIL) |
                                                Q(MOBILE_NUMBER=MOBILE_NUMBER) |
                                                Q(SECONDARY_EMAIL=SECONDARY_EMAIL) |
                                                Q(SECONDARY_EMAIL=EMAIL)))
            if len(obj_cand) > 0:
                # messages.warning(request, "Candidate already exists !!!")
                context['obj_candidate'] = obj_cand
                context['form'] = NewCandidateForm(request.POST, request.FILES)
                return render(request, 'recruitment/new_candidate.html', context)
            else:
                # form.save()
                # obj = form.save(commit=False)
                obj.save()
                id = obj.pk
                context['id'] = id
                obj_candidate = Candidate.objects.get(id=id)
                # Converting to upper case
                obj_candidate.FIRST_NAME = obj_candidate.FIRST_NAME.upper() if obj_candidate.FIRST_NAME else None
                obj_candidate.LAST_NAME = obj_candidate.LAST_NAME.upper() if obj_candidate.LAST_NAME else None
                obj_candidate.LOCATION = obj_candidate.LOCATION.upper() if obj_candidate.LOCATION else None
                obj_candidate.PAN_NUMBER = obj_candidate.PAN_NUMBER.upper() if obj_candidate.PAN_NUMBER else None
                year = date.today().strftime('%y')
                month = date.today().strftime('%m')
                obj_candidate.CANDIDATE_ID = 'CN' + str(id).zfill(4)
                if intStatus == 'Interested':
                    obj_candidate.CANDIDATE_STATUS = "APPROVAL PENDING"
                if intStatus == 'Not Interested':
                    obj_candidate.CANDIDATE_STATUS = "NOT INTERESTED"
                obj_candidate.CREATED_BY = request.user.username
                obj_emp = Employee.objects.get(EMPLOYEE_CODE=request.user.username)
                obj_candidate.RECRUITER = obj_emp
                obj_candidate.RECRUITER_CODE = request.user.username
                obj_candidate.save()
                obj_candidate = Candidate.objects.get(id=id)
                context['form'] = NewCandidateForm(instance=obj_candidate)
                context['obj_candidate'] = obj_candidate
                context['activeTab_No'] = 1
                messages.success(request, f"Candidate has been added !!! Candidate ID is {obj_candidate.CANDIDATE_ID}")
                # return render(request, 'recruitment/new_candidate.html', context)
                # return HttpResponseRedirect(f'/recruitment/candidate/{id}/details/')
                return HttpResponseRedirect(reverse(candidates))
        else:
            context['form'] = NewCandidateForm(request.POST, request.FILES)
            messages.warning(request, form.errors)
            return render(request, 'recruitment/new_candidate.html', context)
    return render(request, 'recruitment/new_candidate.html', context)


@login_required
def edit_candidate(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    form = NewCandidateForm(instance=obj_candidate)
    if request.user.is_superuser:
        obj_job = Job.objects.all().order_by('-TIMESTAMP')
    else:
        obj_job = Job.objects.filter(ASSIGNED_SPOC__EMPLOYEE_CODE=request.user.username).order_by('-TIMESTAMP')
    context = {
        'form': form,
        'obj_job': obj_job,
        'obj_candidate': obj_candidate,
    }
    if request.method == 'POST':
        form = NewCandidateForm(request.POST, request.FILES, instance=obj_candidate)
        if form.is_valid():
            # Check if candidate is above 18 years
            DATE_OF_BIRTH = form.cleaned_data['DATE_OF_BIRTH']
            age = getAge(DATE_OF_BIRTH)
            if age < 18 :
                messages.warning(request, "Date of Birth looks invalid. It is below 18 !!!")
                context['form'] = NewCandidateForm(request.POST, request.FILES, instance=obj_candidate)
                return render(request, 'recruitment/edit_candidate.html', context)
            form.save()
            obj_candidate = Candidate.objects.get(id=id)
            # Converting to upper case
            obj_candidate.FIRST_NAME = obj_candidate.FIRST_NAME.upper() if obj_candidate.FIRST_NAME else None
            obj_candidate.LAST_NAME = obj_candidate.LAST_NAME.upper() if obj_candidate.LAST_NAME else None
            obj_candidate.LOCATION = obj_candidate.LOCATION.upper() if obj_candidate.LOCATION else None
            obj_candidate.PAN_NUMBER = obj_candidate.PAN_NUMBER.upper() if obj_candidate.PAN_NUMBER else None
            obj_candidate.MODIFIED_BY = request.user.username
            obj_candidate.LAST_MODIFIED = now()
            obj_candidate.save()
            obj_candidate = Candidate.objects.get(id=id)
            context['form'] = NewCandidateForm(instance=obj_candidate)
            context['obj_candidate'] = obj_candidate
            context['activeTab_No'] = 1
            messages.success(request, f"Data has been updated !!!")
            # return render(request, 'recruitment/edit_candidate.html', context)
            # return HttpResponseRedirect(f'/recruitment/candidate/{id}/details/')
            return HttpResponseRedirect(reverse(candidates))
        else:
            context['form'] = NewCandidateForm(request.POST, request.FILES, instance=obj_candidate)
            messages.warning(request, form.errors)
            return render(request, 'recruitment/edit_candidate.html', context)
    return render(request, 'recruitment/edit_candidate.html', context)


@login_required
def job_details_view(request, id=None):
    obj_job = Job.objects.get(id=id)
    context = {
        'obj_job': obj_job,
    }
    return render(request, 'recruitment/job_details_view.html', context)


@login_required
def candidates(request):
    if request.user.roles >= 4:
        obj_candidate = Candidate.objects.exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").order_by('-LAST_MODIFIED')
    else:
        obj_candidate = Candidate.objects.filter(Q(RECRUITER__EMPLOYEE_CODE=request.user.username)|
                                                 Q(RECRUITER__REPORTING_MANAGER_CODE=request.user.username)).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").order_by('-LAST_MODIFIED')

    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchBy = request.GET.get('SEARCH_BY')
        searchText = request.GET.get('SEARCH_TEXT')
        if searchBy == 'CANDIDATE_ID':
            obj_candidate = Candidate.objects.filter(CANDIDATE_ID=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").order_by('-TIMESTAMP')
        if searchBy == 'CANDIDATE_NAME':
            obj_candidate = Candidate.objects.filter(Q(FIRST_NAME__icontains=searchText) |
                                                     Q(LAST_NAME__icontains=searchText)).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_ID':
            obj_candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_CODE=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_NAME':
            obj_candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_FULL_NAME__icontains=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_CODE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_CODE=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_NAME':
            obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_NAME__icontains=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_CODE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__JOB_CODE=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_TITLE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__JOB_TITLE__icontains=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'PAN_NUMBER':
            obj_candidate = Candidate.objects.filter(PAN_NUMBER=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'MOBILE_NUMBER':
            obj_candidate = Candidate.objects.filter(MOBILE_NUMBER=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'EMAIL':
            obj_candidate = Candidate.objects.filter(EMAIL=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'SOURCE':
            obj_candidate = Candidate.objects.filter(SOURCE=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
        if searchBy == 'SKILLS':
            obj_candidate = Candidate.objects.filter(SKILL_SET__icontains=searchText).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')
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
                                                     Q(SKILL_SET__icontains=searchText) |
                                                     Q(PAN_NUMBER=searchText)).exclude(CANDIDATE_STATUS="APPLICATION SUBMITTED").distinct().order_by('-TIMESTAMP')

    obj_interview = Interview.objects.all()
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
        'obj_interview': obj_interview,
        'form': SearchCandidateForm(request.GET),
    }
    return render(request, 'recruitment/candidate_list.html', context)


@login_required
def work_list(request):
    obj_emp = Employee.objects.filter(EMPLOYEE_CODE=request.user.username).first()
    if request.user.is_superuser:
        obj_candidate = Candidate.objects.filter(CANDIDATE_STATUS='APPROVAL PENDING').order_by('-TIMESTAMP')
    else:
        if obj_emp:
            # obj_candidate = Candidate.objects.filter(JOB_CODE__SKILL=obj_emp.CATEGORY).order_by('-TIMESTAMP')
            obj_candidate = Candidate.objects.filter(CANDIDATE_STATUS='APPROVAL PENDING').order_by('-TIMESTAMP')
        else:
            obj_candidate = Candidate.objects.none()
    if not request.user.roles >= 2:
        obj_candidate = Candidate.objects.none()

    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchBy = request.GET.get('SEARCH_BY')
        searchText = request.GET.get('SEARCH_TEXT')
        if searchBy == 'CANDIDATE_ID':
            obj_candidate = Candidate.objects.filter(CANDIDATE_ID=searchText).order_by('-TIMESTAMP')
        if searchBy == 'CANDIDATE_NAME':
            obj_candidate = Candidate.objects.filter(Q(FIRST_NAME__icontains=searchText) |
                                                     Q(LAST_NAME__icontains=searchText)).distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_ID':
            obj_candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_NAME':
            obj_candidate = Candidate.objects.filter(RECRUITER__EMPLOYEE_FULL_NAME__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_CODE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_NAME':
            obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_NAME__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_CODE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__JOB_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_TITLE':
            obj_candidate = Candidate.objects.filter(JOB_CODE__JOB_TITLE__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'PAN_NUMBER':
            obj_candidate = Candidate.objects.filter(PAN_NUMBER=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'MOBILE_NUMBER':
            obj_candidate = Candidate.objects.filter(MOBILE_NUMBER=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'EMAIL':
            obj_candidate = Candidate.objects.filter(EMAIL=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'SOURCE':
            obj_candidate = Candidate.objects.filter(SOURCE=searchText).distinct().order_by('-TIMESTAMP')
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
                                              Q(PAN_NUMBER=searchText)).distinct().order_by('-TIMESTAMP')

    page = request.GET.get('page', 1)
    paginator = Paginator(obj_candidate, 50)
    try:
        obj_candidate = paginator.page(page)
    except PageNotAnInteger:
        obj_candidate = paginator.page(1)
    except EmptyPage:
        obj_candidate = paginator.page(paginator.num_pages)
    return render(request, 'recruitment/work_list.html', context={'obj_candidate': obj_candidate, 'form': SearchCandidateForm(request.GET)})


@login_required
def approve_candidate(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    if request.method == 'POST':
        obj_candidate.CANDIDATE_STATUS = "CV APPROVED"
        obj_candidate.CV_APPROVE_DATE = now().date()
        obj_candidate.CV_APPROVE_BY = request.user.username
        obj_candidate.save()
        messages.success(request, "Candidate has been approved !!!")
        return HttpResponseRedirect('/recruitment/work_list/')


@login_required
def reject_candidate(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    if request.method == 'POST':
        obj_candidate.CANDIDATE_STATUS = "CV REJECTED"
        obj_candidate.CV_REJECT_BY = request.user.username
        obj_candidate.save()
        messages.success(request, "Candidate has been rejected !!!")
        return HttpResponseRedirect('/recruitment/work_list/')


@login_required
def not_interested_candidate(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    if request.method == 'POST':
        obj_candidate.CANDIDATE_STATUS = "NOT INTERESTED"
        obj_candidate.JOB_CODE = None
        obj_candidate.MODIFIED_BY = request.user.username
        obj_candidate.LAST_MODIFIED = now()
        obj_candidate.save()
        messages.success(request, "Candidate has been marked as not interested !!!")
        return HttpResponseRedirect('/recruitment/work_list/')


@login_required
def resume_download(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    docs_path = os.path.join(settings.MEDIA_ROOT, str(obj_candidate.RESUME))
    if os.path.exists(docs_path):
        with open(docs_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(docs_path)
            return response
    raise Http404


@login_required
def load_spocs(request):
    candidate_id = request.GET.get('candidate')
    obj_cand = Candidate.objects.get(id=candidate_id)
    client_id = obj_cand.JOB_CODE.CLIENT_CODE.id
    spocs = ClientSPOC.objects.filter(CUSTOMER__id=client_id)
    return render(request, 'recruitment/spoc_dropdown_list_options.html', {'spocs': spocs})


@login_required
def schedule_interview(request, id=None):
    if request.user.roles >= 4:
        obj_candidate = Candidate.objects.all().exclude(CANDIDATE_STATUS="APPROVAL PENDING").order_by('-TIMESTAMP')
    else:
        obj_candidate = Candidate.objects.filter((Q(RECRUITER__EMPLOYEE_CODE=request.user.username) |
                                                 Q(RECRUITER__REPORTING_MANAGER_CODE=request.user.username)) &
                                                 (Q(CANDIDATE_STATUS__contains='SELECT') |
                                                  Q(CANDIDATE_STATUS__contains='APPROVED'))).exclude(CANDIDATE_STATUS="APPROVAL PENDING").order_by('-TIMESTAMP')
    context = {
        'form': InterviewForm(),
        'obj_candidate': obj_candidate,
    }
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            # form.save()
            candidate = form.cleaned_data['CANDIDATE']
            obj_interview = Interview.objects.filter(CANDIDATE__id=candidate.id)
            interview_round = form.cleaned_data['INTERVIEW_ROUND']
            for item in obj_interview:
                if interview_round == item.INTERVIEW_ROUND:
                    context['form'] = InterviewForm(request.POST)
                    messages.warning(request, f"{item.INTERVIEW_ROUND} interview already scheduled for this candidate !!!")
                    return render(request, 'recruitment/schedule_interview.html', context)
            obj = form.save(commit=False)
            obj.save()
            id = obj.pk
            context['id'] = id
            obj_interview = Interview.objects.get(id=id)
            obj_interview.INTERVIEW_ID = 'IN' + str(id).zfill(4)
            obj_interview.INTERVIEW_STATUS = "IN-PROCESS"
            obj_interview.CREATED_BY = request.user.username
            obj_interview.save()
            obj_interview = Interview.objects.get(id=id)
            if obj_interview.CANDIDATE.CANDIDATE_STATUS:
                pass
            else:
                obj_interview.CANDIDATE.CANDIDATE_STATUS = "INTERVIEW SCHEDULED"
            obj_interview.CANDIDATE.INTERVIEW_SCHEDULED = True
            obj_interview.CANDIDATE.save()
            context['form'] = InterviewForm(instance=obj_interview)
            context['obj_interview'] = obj_interview
            context['activeTab_No'] = 1
            messages.success(request, f"Interview has been scheduled !!! Interview ID is {obj_interview.INTERVIEW_ID}")
            # return render(request, 'recruitment/create_details.html', context)
            context['form'] = InterviewForm()
            return render(request, 'recruitment/schedule_interview.html', context)
        else:
            context['form'] = InterviewForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'recruitment/schedule_interview.html', context)
    return render(request, 'recruitment/schedule_interview.html', context)


@login_required
def interviews(request):
    if request.user.roles >= 4:
        obj_interview = Interview.objects.all().order_by('-TIMESTAMP')
    else:
        obj_interview = Interview.objects.filter(Q(CANDIDATE__RECRUITER__EMPLOYEE_CODE=request.user.username) |
                                                 Q(CANDIDATE__RECRUITER__REPORTING_MANAGER_CODE=request.user.username)).order_by('-TIMESTAMP')

    if (request.method == 'GET') and ('btn_search' in request.GET):
        searchBy = request.GET.get('SEARCH_BY')
        searchText = request.GET.get('SEARCH_TEXT')
        if searchBy == 'INTERVIEW_ID':
            obj_interview = Interview.objects.filter(INTERVIEW_ID=searchText).order_by('-TIMESTAMP')
        if searchBy == 'CANDIDATE_ID':
            obj_interview = Interview.objects.filter(CANDIDATE__CANDIDATE_ID=searchText).order_by('-TIMESTAMP')
        if searchBy == 'CANDIDATE_NAME':
            obj_interview = Interview.objects.filter(Q(CANDIDATE__FIRST_NAME__icontains=searchText) |
                                                     Q(CANDIDATE__LAST_NAME__icontains=searchText)).distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_ID':
            obj_interview = Interview.objects.filter(CANDIDATE__RECRUITER__EMPLOYEE_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'RECRUITER_NAME':
            obj_interview = Interview.objects.filter(CANDIDATE__RECRUITER__EMPLOYEE_FULL_NAME__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_CODE':
            obj_interview = Interview.objects.filter(CANDIDATE__JOB_CODE__CLIENT_CODE__CUSTOMER_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'CUSTOMER_NAME':
            obj_interview = Interview.objects.filter(CANDIDATE__JOB_CODE__CLIENT_CODE__CUSTOMER_NAME__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_CODE':
            obj_interview = Interview.objects.filter(CANDIDATE__JOB_CODE__JOB_CODE=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'JOB_TITLE':
            obj_interview = Interview.objects.filter(CANDIDATE__JOB_CODE__JOB_TITLE__icontains=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'PAN_NUMBER':
            obj_interview = Interview.objects.filter(CANDIDATE__PAN_NUMBER=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'MOBILE_NUMBER':
            obj_interview = Interview.objects.filter(CANDIDATE__MOBILE_NUMBER=searchText).distinct().order_by('-TIMESTAMP')
        if searchBy == 'EMAIL':
            obj_interview = Interview.objects.filter(CANDIDATE__EMAIL=searchText).distinct().order_by('-TIMESTAMP')
        if not searchBy:
            obj_interview = Interview.objects.filter(Q(INTERVIEW_ID=searchText) |
                                                     Q(CANDIDATE__FIRST_NAME__icontains=searchText) |
                                                     Q(CANDIDATE__LAST_NAME__icontains=searchText) |
                                                     Q(CANDIDATE__RECRUITER__EMPLOYEE_CODE=searchText) |
                                                     Q(CANDIDATE__JOB_CODE__JOB_CODE=searchText) |
                                                     Q(CANDIDATE__JOB_CODE__JOB_TITLE__icontains=searchText) |
                                                     Q(CANDIDATE__EMAIL=searchText) |
                                                     Q(CANDIDATE__MOBILE_NUMBER=searchText) |
                                                     Q(CANDIDATE__PAN_NUMBER=searchText)).distinct().order_by('-TIMESTAMP')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_interview, 50)
    try:
        obj_interview = paginator.page(page)
    except PageNotAnInteger:
        obj_interview = paginator.page(1)
    except EmptyPage:
        obj_interview = paginator.page(paginator.num_pages)
    return render(request, 'recruitment/interview_list.html', context={'obj_interview': obj_interview, 'form': SearchInterviewForm(request.GET)})


@login_required
def interview_details(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    obj_interview = Interview.objects.filter(CANDIDATE=obj_candidate).order_by('-TIMESTAMP')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_interview, 10)
    try:
        obj_interview = paginator.page(page)
    except PageNotAnInteger:
        obj_interview = paginator.page(1)
    except EmptyPage:
        obj_interview = paginator.page(paginator.num_pages)
    return render(request, 'recruitment/interview_list.html', context={'obj_interview': obj_interview})


@login_required
def update_interview_status(request, id=None):
    obj_interview = Interview.objects.get(id=id)
    form = InterviewStatusForm()
    context = {
        'obj_interview': obj_interview,
        'form': form,
    }
    if request.method == 'POST':
        form = InterviewStatusForm(request.POST, instance=obj_interview)
        if form.is_valid():
            obj = form.save(commit=False)
            INTERVIEW_STATUS = form.cleaned_data['INTERVIEW_STATUS']
            CANDIDATE_STATUS = form.cleaned_data['CANDIDATE_STATUS']
            INTERVIEW_ROUND = form.cleaned_data['INTERVIEW_ROUND']
            INTERVIEW_COMMENTS = form.cleaned_data['INTERVIEW_COMMENTS']
            obj_interview = Interview.objects.get(id=id)
            obj_interview.INTERVIEW_STATUS = INTERVIEW_STATUS
            obj_interview.INTERVIEW_ROUND = INTERVIEW_ROUND
            obj_interview.INTERVIEW_COMMENTS = INTERVIEW_COMMENTS
            obj_interview.save()
            if (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'SELECT'):
                obj_interview.CANDIDATE.CANDIDATE_STATUS = INTERVIEW_ROUND + ' ROUND SELECTED'
            if (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'REJECT'):
                obj_interview.CANDIDATE.CANDIDATE_STATUS = INTERVIEW_ROUND + ' ROUND REJECTED'
            if INTERVIEW_STATUS != 'COMPLETED':
                obj_interview.CANDIDATE.CANDIDATE_STATUS = INTERVIEW_STATUS
            obj_interview.CANDIDATE.save()
            messages.success(request, "Interview status has been updated !!!")
            return HttpResponseRedirect(reverse(interviews))
    return render(request, 'recruitment/update_interview_status.html', context)


@login_required
def candidate_details(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    obj_interview = Interview.objects.filter(CANDIDATE=obj_candidate).order_by('-TIMESTAMP')
    context = {
        'obj_candidate': obj_candidate,
        'obj_interview': obj_interview
    }
    return render(request, 'recruitment/candidate_details_view.html', context)


@login_required
def interview_details_view(request, id=None):
    obj_interview = Interview.objects.get(id=id)
    context = {
        'obj_interview': obj_interview
    }
    return render(request, 'recruitment/interview_details_view.html', context)


@login_required
def update_candidate_status(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    obj_my_candidate = Candidate.objects.filter(Q(RECRUITER__EMPLOYEE_CODE=request.user.username) |
                                                Q(RECRUITER__REPORTING_MANAGER_CODE=request.user.username)).order_by('-TIMESTAMP')
    if request.method == 'POST':
        status = request.POST['status']
        statusRemarks = request.POST['statusRemarks']
        expectedDOJ = request.POST['expectedDOJ']
        finalDOJ = request.POST['finalDOJ']
        dropOutReason = request.POST['dropOutReason']
        obj_interview = Interview.objects.filter(CANDIDATE__id=obj_candidate.id)
        if obj_interview.count() <= 0:
            messages.warning(request, "Need to schedule interview first !!!")
            return HttpResponseRedirect(reverse(candidates))

        interview_date = []
        for item in obj_interview:
            if (item.INTERVIEW_STATUS == 'IN-PROCESS') or (item.INTERVIEW_STATUS == 'ON-HOLD') or (item.INTERVIEW_STATUS == 'PENDING'):
                messages.warning(request, f"Candidate interview is {item.INTERVIEW_STATUS}. Need to complete interview first !!!")
                return HttpResponseRedirect(reverse(candidates))

            if 'REJECT' in obj_candidate.CANDIDATE_STATUS:
                messages.warning(request, "Cannot update the status. Candidate is REJECTED !!!")
                return HttpResponseRedirect(reverse(candidates))

            interview_date.append(item.INTERVIEW_DATE)
        max_interview_date = max(interview_date)
        if (status == 'FINAL SELECT') or (status == 'OFFERED'):
            expectedDOJ = datetime.strptime(expectedDOJ, "%Y-%m-%d").date()
            if expectedDOJ < max_interview_date:
                messages.warning(request, "Invalid EXPECTED DOJ. It cannot be less than interviews date !!!")
                return HttpResponseRedirect(reverse(candidates))
            if finalDOJ:
                finalDOJ = datetime.strptime(finalDOJ, "%Y-%m-%d").date()
                if finalDOJ < expectedDOJ:
                    messages.warning(request, "Invalid FINAL DOJ. It cannot be less than EXPECTED DOJ !!!")
                    return HttpResponseRedirect(reverse(candidates))
        if status == 'JOINED':
            finalDOJ = datetime.strptime(finalDOJ, "%Y-%m-%d").date()
            expectedDOJ = obj_candidate.EXPECTED_DOJ
            if finalDOJ < max_interview_date:
                messages.warning(request, "Invalid FINAL DOJ. It cannot be less than interviews date !!!")
                return HttpResponseRedirect(reverse(candidates))
            if expectedDOJ:
                if finalDOJ < expectedDOJ:
                    messages.warning(request, "Invalid FINAL DOJ. It cannot be less than EXPECTED DOJ !!!")
                    return HttpResponseRedirect(reverse(candidates))
        obj_candidate.CANDIDATE_STATUS = status
        if obj_candidate.BILLING_STATUS == "NOT APPLICABLE":
            obj_candidate.BILLING_STATUS = "INVOICE PENDING"
        if statusRemarks:
            obj_candidate.CANDIDATE_STATUS_REMARKS = statusRemarks
        if expectedDOJ:
            obj_candidate.EXPECTED_DOJ = expectedDOJ
        if finalDOJ:
            obj_candidate.FINAL_DOJ = finalDOJ
        if dropOutReason:
            obj_candidate.DROP_OUT_REASON = dropOutReason

        obj_candidate.save()
        messages.success(request, "Status has been updated !!!")
        return HttpResponseRedirect(reverse(candidates))
