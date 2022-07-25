from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('new/', employee_registration, name='employee_registration'),
    path('<int:id>/details/', employee_info, name='employee_info'),
    path('<int:id>/details/ajax/emp_name/', search_emp, name='search_emp'),
    path('download/<int:id>/', download_emp_docs, name='download_emp_docs'),
    path('employee_list/', employee_list, name='employee_list'),
    path('<int:id>/view/', emp_view, name='emp_view'),
]
