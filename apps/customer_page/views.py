from django.shortcuts import render, HttpResponseRedirect, reverse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.recruitment.models import Candidate, Job, Interview
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
import os
from apps.recruitment.forms import InterviewStatusForm


@login_required
def client_interviews(request):
    obj_interview = Interview.objects.filter(CANDIDATE__JOB_CODE__CLIENT_CODE__CUSTOMER_CODE=request.user.username).order_by('-TIMESTAMP')
    # obj_job = Job.objects.filter(CLIENT_CODE__CUSTOMER_CODE=request.user.username).first()
    # obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE_id=obj_job.id).order_by('-TIMESTAMP')
    form = InterviewStatusForm()
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_interview, 10)
    try:
        obj_interview = paginator.page(page)
    except PageNotAnInteger:
        obj_interview = paginator.page(1)
    except EmptyPage:
        obj_interview = paginator.page(paginator.num_pages)
    return render(request, 'customer_page/interviews.html', {'obj_interview': obj_interview, 'form': form})


@login_required
def client_candidates(request, id=None):
    obj_candidate = Candidate.objects.filter(JOB_CODE__CLIENT_CODE__CUSTOMER_CODE=request.user.username, INTERVIEW_SCHEDULED=True).order_by('-TIMESTAMP')
    # id_list = Candidate.objects.values_list('id').distinct()
    # obj_interview = Interview.objects.filter(CANDIDATE__in=id_list)
    obj_interview = Interview.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_candidate, 10)
    try:
        obj_candidate = paginator.page(page)
    except PageNotAnInteger:
        obj_candidate = paginator.page(1)
    except EmptyPage:
        obj_candidate = paginator.page(paginator.num_pages)
    return render(request, 'customer_page/candidates.html', {'obj_candidate': obj_candidate, 'obj_interview': obj_interview})


# @login_required
# def reject_candidate(request, id=None):
#     obj_candidate = Candidate.objects.get(id=id)
#     if request.method == 'POST':
#         obj_candidate.CANDIDATE_STATUS = "CLIENT REJECTED"
#         obj_candidate.save()
#         messages.success(request, "Candidate has been rejected !!!")
#         return HttpResponseRedirect('/customer/candidate/')


@login_required
def resume_client_download(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    docs_path = os.path.join(settings.MEDIA_ROOT, str(obj_candidate.RESUME))
    if os.path.exists(docs_path):
        with open(docs_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename='+os.path.basename(docs_path)
            return response
    raise Http404


# @login_required
# def update_statusCopy(request, id=None):
#     obj_interview = Interview.objects.get(id=id)
#     form = InterviewStatusForm()
#     context = {
#        'obj_interview': obj_interview,
#         'form': form,
#     }
#     if request.method == 'POST':
#         form = InterviewStatusForm(request.POST, instance=obj_interview)
#         id = request.POST['interview_id']
#         if form.is_valid():
#             obj = form.save(commit=False)
#             INTERVIEW_STATUS = form.cleaned_data['INTERVIEW_STATUS']
#             CANDIDATE_STATUS = form.cleaned_data['CANDIDATE_STATUS']
#             INTERVIEW_ROUND = form.cleaned_data['INTERVIEW_ROUND']
#             INTERVIEW_COMMENTS = form.cleaned_data['INTERVIEW_COMMENTS']
#             obj_interview = Interview.objects.get(id=id)
#             obj_interview.INTERVIEW_STATUS = INTERVIEW_STATUS
#             obj_interview.INTERVIEW_ROUND = INTERVIEW_ROUND
#             obj_interview.INTERVIEW_COMMENTS = INTERVIEW_COMMENTS
#             obj_interview.save()
#             if (INTERVIEW_ROUND == 'HR ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'SELECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'HR SELECT'
#             if (INTERVIEW_ROUND == 'HR ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'REJECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'HR REJECT'
#             if (INTERVIEW_ROUND == 'TR ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'SELECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'TR SELECT'
#             if (INTERVIEW_ROUND == 'TR ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'REJECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'TR REJECT'
#             if (INTERVIEW_ROUND == 'MR ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'SELECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'MR SELECT'
#             if (INTERVIEW_ROUND == 'MR ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'REJECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'MR REJECT'
#             if (INTERVIEW_ROUND == 'V&A ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'SELECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'V&A SELECT'
#             if (INTERVIEW_ROUND == 'V&A ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'REJECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'V&A REJECT'
#             if (INTERVIEW_ROUND == 'APTITUDE-TEST ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'SELECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'APTITUDE-TEST SELECT'
#             if (INTERVIEW_ROUND == 'APTITUDE-TEST ROUND') and (INTERVIEW_STATUS == 'COMPLETED') and (CANDIDATE_STATUS == 'REJECT'):
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = 'APTITUDE-TEST REJECT'
#             if INTERVIEW_STATUS != 'COMPLETED':
#                 obj_interview.CANDIDATE.CANDIDATE_STATUS = INTERVIEW_STATUS
#             obj_interview.CANDIDATE.save()
#             messages.success(request, "Interview status has been updated !!!")
#             return HttpResponseRedirect(reverse(client_interviews))
#     return render(request, 'customer_page/interviews.html', context)


@login_required
def update_status(request, id=None):
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
            return HttpResponseRedirect(reverse(client_interviews))
    return render(request, 'customer_page/update_interview_status.html', context)
