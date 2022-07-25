from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', download_page, name='download_page'),
    path('job_master/', export_job_master, name='export_job_master'),
    path('candidate_master/', export_candidate_master, name='export_candidate_master'),
    path('interview_master/', export_interview_master, name='export_interview_master'),
    path('employee_master/', export_employee_master, name='export_employee_master'),
    path('client_master/', export_client_master, name='export_client_master'),
]
