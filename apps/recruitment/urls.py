from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('job/', job_list, name='job_list'),
    path('job/<int:id>/details/', job_details, name='job_details'),
    path('job/<int:id>/view/', job_details_view, name='job_details_view'),
    path('job/<int:id>/clone_job/', clone_job, name='clone_job'),
    path('assigned_job/', assigned_job, name='assigned_job'),
    path('work_list/', work_list, name='work_list'),
    path('work_list/<int:id>/approve/', approve_candidate, name='approve_candidate'),
    path('work_list/<int:id>/reject/', reject_candidate, name='reject_candidate'),
    path('resume_download/<int:id>/', resume_download, name='resume_download'),
    path('job/create_job/', create_job, name='create_job'),
    path('candidates/', candidates, name='candidates'),
    path('candidates/<int:id>/update/', update_candidate_status, name='update_candidate_status'),
    # path('candidates/<int:id>/interviews/', interview_details, name='interview_details'),
    path('candidates/new_candidate/', new_candidate, name='new_candidate'),
    path('candidates/<int:id>/details/', edit_candidate, name='edit_candidate'),
    path('candidates/<int:id>/view/', candidate_details, name='candidate_details'),
    path('interviews/', interviews, name='interviews'),
    path('interviews/<int:id>/view/', interview_details_view, name='interview_details_view'),
    path('interviews/<int:id>/update/', update_interview_status, name='update_interview_status'),
    path('interviews/schedule_interview/', schedule_interview, name='schedule_interview'),
    path('ajax/load-spocs/', load_spocs, name='ajax_load_spocs'),
]
