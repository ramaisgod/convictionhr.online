from django.db import models
from .choices import *
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
import os
from convictionhr_master.choices import *


class Client(models.Model):
    CUSTOMER_CODE = models.CharField(max_length=5, unique=True, editable=False)
    CUSTOMER_NAME = models.CharField(max_length=255)
    CUSTOMER_START_DATE = models.DateField(blank=True, null=True)
    CONTRACT_START_DATE = models.DateField(blank=True, null=True)
    CONTRACT_END_DATE = models.DateField(blank=True, null=True)
    CORPORATE_ADDRESS = models.CharField(max_length=255, blank=True, null=True)
    CORPORATE_CITY = models.CharField(max_length=255, blank=True, null=True)
    CORPORATE_STATE = models.CharField(max_length=255, blank=True, null=True)
    CORPORATE_PINCODE = models.CharField(max_length=6, blank=True, null=True)
    CORPORATE_COUNTRY = models.CharField(max_length=255, blank=True, null=True)
    BOTH_ADDRESS_SAME = models.CharField(max_length=20, blank=True, null=True)
    BILLING_ADDRESS = models.CharField(max_length=255, blank=True, null=True)
    BILLING_CITY = models.CharField(max_length=255, blank=True, null=True)
    BILLING_STATE = models.CharField(max_length=255, blank=True, null=True)
    BILLING_PINCODE = models.CharField(max_length=6, blank=True, null=True)
    BILLING_COUNTRY = models.CharField(max_length=255, blank=True, null=True)
    MSMED_NUMBER = models.CharField(max_length=255, blank=True, null=True)
    POTENTIAL_CUSTOMER = models.CharField(max_length=255, blank=True, null=True, choices=CHOICE_YES_NO)
    SKILL = models.CharField(max_length=255, blank=True, null=True, choices=CHOICE_SKILL)
    # SUB_SKILL = models.CharField(max_length=255, blank=True, null=True)
    LOCATION_SERVE = models.CharField(max_length=255, blank=True, null=True)
    GSTIN_NUMBER = models.CharField(max_length=15, blank=True, null=True)
    PAN_NUMBER = models.CharField(max_length=10, blank=True, null=True)
    REGISTERED_ON = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False)
    REGISTERED_BY = models.CharField(max_length=10, null=True, blank=True)
    MODIFIED_BY = models.CharField(max_length=10, null=True, blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.CUSTOMER_CODE) + " - " + str(self.CUSTOMER_NAME)


class ClientSPOC(models.Model):
    CUSTOMER = models.ForeignKey(Client, on_delete=models.CASCADE)
    LOCATION = models.CharField(max_length=255, blank=True, null=True)
    PERSON_NAME = models.CharField(max_length=100)
    EMAIL = models.EmailField(max_length=150, blank=True, null=True)
    CONTACT = models.CharField(max_length=30, blank=True, null=True)
    TYPE = models.CharField(max_length=255, blank=True, null=True, choices=CHOICE_SPOC_TYPE)
    TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.PERSON_NAME) + " - " + str(self.TYPE)


def get_upload_path(instance, filename):
    return os.path.join('Client//'+str(instance.CUSTOMER_CODE.CUSTOMER_CODE), filename)


class ClientDocuments(models.Model):
    CUSTOMER_CODE = models.ForeignKey(Client, on_delete=models.CASCADE)
    DOCUMENT_TITLE = models.CharField(max_length=100)
    # DOCUMENTS = models.FileField(upload_to='Client/', validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'xls', 'xlsx', 'pdf', 'zip', 'jpg', 'jpeg', 'png', 'ppt', 'pptx'])])
    DOCUMENTS = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'xls', 'xlsx', 'pdf', 'zip', 'jpg', 'jpeg', 'png', 'ppt', 'pptx'])])
    UPLOAD_TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    UPLOADED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.CUSTOMER_CODE)
