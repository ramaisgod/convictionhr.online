from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('new/', client_registration, name='client_registration'),
    path('client_list/', client_list, name='client_list'),
    path('<int:id>/details/', client_info, name='client_info'),
    path('<int:id>/view/', client_view, name='client_view'),
    path('download/<int:id>/', download_docs, name='download_docs'),
    path('spoc/new/', add_new_spoc, name='add_new_spoc'),
    path('spoc/<int:id>/details/', spoc_info, name='spoc_info'),
]
