from django.shortcuts import render
from django.http import HttpResponse
from .resources import *
from django.utils.timezone import now
import csv


def download_page(request):
    return render(request, 'reports/download_page.html', {})


def export_candidate_master(request):
    resource = CandidateResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    filename = f"candidate_master{now().strftime('%d%m%Y%H%M%S')}.csv"
    response['Content-Disposition'] = "attachment; filename="+filename
    return response


def export_interview_master(request):
    resource = InterviewResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    filename = f"interview_master{now().strftime('%d%m%Y%H%M%S')}.csv"
    response['Content-Disposition'] = "attachment; filename="+filename
    return response


def export_job_master(request):
    resource = JobResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    filename = f"job_master{now().strftime('%d%m%Y%H%M%S')}.csv"
    response['Content-Disposition'] = "attachment; filename="+filename
    return response


def export_employee_master(request):
    resource = EmployeeResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    filename = f"employee_master{now().strftime('%d%m%Y%H%M%S')}.csv"
    response['Content-Disposition'] = "attachment; filename="+filename
    return response


def export_client_master(request):
    resource = ClientResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    filename = f"client_master{now().strftime('%d%m%Y%H%M%S')}.csv"
    response['Content-Disposition'] = "attachment; filename="+filename
    return response

