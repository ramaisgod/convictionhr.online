from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('pending_list/', pending_for_invoice, name='ready_for_billing'),
    path('create_invoice/<int:id>/', create_new_invoice, name='create_new_invoice'),
    path('invoices/', invoice_list, name='invoice_list'),
]
