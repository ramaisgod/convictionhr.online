from django.urls import path
from .views import *


urlpatterns = [
    path('login/', logout_page, name='logout_page'),
    path('home/', home_page, name='home'),
    path('employee/', emp_page, name='emp'),
    path('create_user/', create_user, name='create_user'),
    path('change_password/', change_password, name='change_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('user_roles/', user_roles, name='user_roles'),
    path('all_users/', all_users, name='all_users'),
    path('online_users/', online_users, name='online_users'),
]
