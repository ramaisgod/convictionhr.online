from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from apps.recruitment.forms import SearchCandidateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.timezone import now
from datetime import date, datetime
from django.db.models import Q
from .forms import *


@login_required
def pending_for_invoice(request):
    context = {
        'form': SearchCandidateForm(request.GET),
    }
    obj_candidate = Candidate.objects.filter(BILLING_STATUS="INVOICE PENDING")
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_candidate, 50)
    try:
        obj_candidate = paginator.page(page)
    except PageNotAnInteger:
        obj_candidate = paginator.page(1)
    except EmptyPage:
        obj_candidate = paginator.page(paginator.num_pages)
    context['obj_candidate'] = obj_candidate
    return render(request, 'billing/ready_for_billing.html', context)


@login_required
def create_new_invoice(request, id=None):
    obj_candidate = Candidate.objects.get(id=id)
    context = {
        'form': NewInvoiceForm(),
        'obj_candidate': obj_candidate,
    }
    if request.method == 'POST':
        form = NewInvoiceForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.CANDIDATE = obj_candidate
            obj.save()
            billing_id = obj.pk
            obj.INVOICE_NUMBER = f"{str(date.today().strftime('%y%m%d')) + str(billing_id).zfill(4)}"
            obj.RAISED_BY = request.user.username
            obj.INVOICE_STATUS = "UNPAID"
            obj.save()
            obj_candidate.BILLING_STATUS = "INVOICE CREATED"
            obj_candidate.save()
            # obj_billing = BillingTracker.objects.get(id=billing_id)
            # Converting to upper case
            # obj_client.PAN_NUMBER = obj_client.PAN_NUMBER.upper() if obj_client.PAN_NUMBER else None
            # obj_client.GSTIN_NUMBER = obj_client.GSTIN_NUMBER.upper() if obj_client.GSTIN_NUMBER else None
            # obj_job.JOB_CODE = 'J' + str(id).zfill(3)
            # obj_job.JOB_OPENING_STATUS = "IN-PROGRESS"
            # obj_job.CREATED_BY = request.user.username
            # obj_job.save()
            # obj_job = Job.objects.get(id=id)
            # context['form'] = JobForm(instance=obj_job)
            # context['obj_job'] = obj_job
            # context['activeTab_No'] = 1
            messages.success(request, f"Invoice has been created !!! Invoice Number is {obj.INVOICE_NUMBER}")
            # return render(request, 'recruitment/create_details.html', context)
            # return HttpResponseRedirect(f'/recruitment/job/{id}/details/')
            return HttpResponseRedirect(reverse(pending_for_invoice))
        else:
            context['form'] = NewInvoiceForm(request.POST)
            messages.warning(request, form.errors)
            return render(request, 'billing/new_invoice.html', context)
    return render(request, 'billing/new_invoice.html', context)


@login_required
def invoice_list(request):
    context = {
        'form': SearchCandidateForm(request.GET),
    }
    obj_billing = BillingTracker.objects.all().order_by('-TIMESTAMP')
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_billing, 50)
    try:
        obj_billing = paginator.page(page)
    except PageNotAnInteger:
        obj_billing = paginator.page(1)
    except EmptyPage:
        obj_billing = paginator.page(paginator.num_pages)
    context['obj_billing'] = obj_billing
    return render(request, 'billing/invoice_list.html', context)
