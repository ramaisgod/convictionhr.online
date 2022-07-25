from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('interviews/', client_interviews, name='client_interviews'),
    path('candidates/', client_candidates, name='client_candidates'),
    # path('interviews/update/', update_status, name='update_status'),
    path('resume_download/<int:id>/', resume_client_download, name='resume_client_download'),
    path('interviews/<int:id>/update/', update_status, name='update_status'),
]
