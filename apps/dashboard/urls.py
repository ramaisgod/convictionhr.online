from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('recruitment/', recruitment_dashboard, name='recruitment_dashboard'),
    path('my_dashboard/', my_dashboard, name='my_dashboard'),
]
