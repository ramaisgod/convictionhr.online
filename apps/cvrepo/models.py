from django.db import models
from django.core.validators import FileExtensionValidator
from .choices import *
import os


def get_upload_path(instance, filename):
    # file_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    first_name = instance.FIRST_NAME
    last_name = instance.LAST_NAME
    pan_number = instance.PAN_NUMBER
    cv_name = ''
    if first_name:
        cv_name = cv_name + "_" + str(first_name).upper()
    if last_name:
        cv_name = cv_name + "_" + str(last_name).upper()
    if pan_number:
        cv_name = cv_name + "_" + str(pan_number).upper()
    return os.path.join('CV_Repository//', cv_name + extension)


class CVRepo(models.Model):
    CV_NUMBER = models.CharField(max_length=15, unique=True, editable=False, null=True, blank=True)
    CANDIDATE_CODE = models.CharField(max_length=100, null=True, blank=True)
    FIRST_NAME = models.CharField(max_length=100, null=True, blank=True)
    LAST_NAME = models.CharField(max_length=100, null=True, blank=True)
    DATE_OF_BIRTH = models.CharField(max_length=100, null=True, blank=True)
    GENDER = models.CharField(max_length=50, blank=True, null=True, choices=CHOICE_GENDER)
    PAN_NUMBER = models.CharField(max_length=10, blank=True, null=True)
    MOBILE_NUMBER = models.CharField(max_length=10, null=True, blank=True)
    ALTERNATE_PHONE = models.CharField(max_length=30, null=True, blank=True)
    EMAIL = models.EmailField(max_length=150, null=True, blank=True)
    SECONDARY_EMAIL = models.EmailField(max_length=150, null=True, blank=True)
    QUALIFICATION = models.CharField(max_length=255, blank=True, null=True)
    WORK_EXPERIENCE = models.CharField(max_length=100, blank=True, null=True)
    CURRENT_LOCATION = models.CharField(max_length=100, null=True, blank=True)
    SKILLS = models.TextField(null=True, blank=True)
    SOURCE = models.CharField(max_length=100, null=True, blank=True)
    SUB_SOURCE = models.CharField(max_length=100, null=True, blank=True)
    DESIGNATION = models.CharField(max_length=100, null=True, blank=True)
    DEPARTMENT = models.CharField(max_length=100, null=True, blank=True)
    GRADE = models.CharField(max_length=100, null=True, blank=True)
    PO_NUMBER = models.CharField(max_length=100, null=True, blank=True)
    REMARKS = models.CharField(max_length=1000, null=True, blank=True)
    CANDIDATE_OWNER = models.CharField(max_length=100, null=True, blank=True)
    RESUME = models.FileField(upload_to='CV_Repository/', blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf'])])
    TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.CV_NUMBER) + " - " + str(self.FIRST_NAME) + " " + str(self.LAST_NAME) if self.LAST_NAME else str(self.CV_NUMBER) + " - " + str(self.FIRST_NAME)
