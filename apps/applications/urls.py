from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('create_profile/<str:emp>/', candidate_profile_upload, name='candidate_profile_upload'),
    path('search/', search, name='search'),
    path('candidate_url/', candidate_url, name='candidate_url'),
    path('update_job_code/<int:id>/', update_job_code, name='update_job_code'),
]
