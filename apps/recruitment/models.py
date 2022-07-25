from django.db import models
from apps.employee.models import Employee
from apps.client.models import Client, ClientSPOC
from .choices import *
from convictionhr_master.choices import *
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator
import os


class Job(models.Model):
    JOB_CODE = models.CharField(max_length=10, unique=True, null=True, blank=True, editable=False)
    CLIENT_CODE = models.ForeignKey(Client, on_delete=models.CASCADE)
    JOB_TITLE = models.CharField(max_length=255, null=True, blank=True)
    NUMBER_OF_POSITIONS = models.PositiveIntegerField(null=True, blank=True)
    JOB_START_DATE = models.DateField(null=True, blank=True)
    TARGET_DATE = models.DateField(null=True, blank=True)
    ASSIGNED_SPOC = models.ManyToManyField(Employee)
    LINE_OF_BUSINESS = models.CharField(max_length=255, null=True, blank=True, choices=CHOICE_LINE_OF_BUSINESS)
    JOB_TYPE = models.CharField(max_length=255, null=True, blank=True, choices=CHOICE_JOB_TYPE)
    PRIORITY_TYPE = models.CharField(max_length=255, null=True, blank=True, choices=CHOICE_PRIORITY)
    WORK_EXPERIENCE = models.CharField(max_length=255, null=True, blank=True)
    JOB_LOCATION = models.CharField(max_length=255, null=True, blank=True)
    JOB_OPENING_STATUS = models.CharField(max_length=255, null=True, blank=True)
    JOB_DESCRIPTION = models.TextField(null=True, blank=True)
    REQUIRED_SKILLS = models.TextField(null=True, blank=True)
    REQUIRED_QUALIFICATION = models.CharField(max_length=255, null=True, blank=True)
    SKILL = models.CharField(max_length=255, null=True, blank=True, choices=CHOICE_SKILL)
    SUB_SKILL = models.CharField(max_length=255, null=True, blank=True)
    JOB_SHIFT = models.CharField(max_length=255, null=True, blank=True, choices=CHOICE_SHIFT)
    NUMBER_OF_POSITIONS_CLOSED = models.CharField(max_length=255, null=True, blank=True)
    NUMBER_OF_CURRENT_POSITIONS = models.CharField(max_length=255, null=True, blank=True)
    NUMBER_OF_PROFILES_SHARED = models.CharField(max_length=255, null=True, blank=True)
    TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    CREATED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)
    MODIFIED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)
    LAST_MODIFIED = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.JOB_CODE) + " - " + str(self.JOB_TITLE)


class SubSkill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


def get_upload_path(instance, filename):
    # file_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    first_name = instance.FIRST_NAME
    last_name = instance.LAST_NAME
    pan_number = instance.PAN_NUMBER
    if last_name:
        filename = "CV_" + str(first_name).upper() + ' ' + str(last_name).upper() + '_' + str(pan_number).upper() + extension
    else:
        filename = "CV_" + str(first_name).upper() + '_' + str(pan_number).upper() + extension
    return os.path.join('Resume//', filename)


class Candidate(models.Model):
    CANDIDATE_ID = models.CharField(max_length=10, unique=True, null=True, blank=True, editable=False)
    JOB_CODE = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    FIRST_NAME = models.CharField(max_length=255)
    LAST_NAME = models.CharField(max_length=255, blank=True, null=True)
    DATE_OF_BIRTH = models.DateField(blank=True, null=True)
    GENDER = models.CharField(max_length=50, blank=True, null=True, choices=CHOICE_GENDER)
    PAN_NUMBER = models.CharField(max_length=10, blank=True, null=True)
    SOURCE = models.CharField(max_length=255, blank=True, null=True)
    SUB_SOURCE = models.CharField(max_length=255, blank=True, null=True)
    EMAIL = models.EmailField(max_length=100, blank=True, null=True)
    SECONDARY_EMAIL = models.EmailField(max_length=100, blank=True, null=True)
    MOBILE_NUMBER = models.CharField(max_length=10, blank=True, null=True)
    ALTERNATE_PHONE = models.CharField(max_length=30, blank=True, null=True)
    QUALIFICATION = models.CharField(max_length=255, blank=True, null=True)
    WORK_EXPERIENCE = models.CharField(max_length=100, blank=True, null=True)
    LOCATION = models.CharField(max_length=255, blank=True, null=True)
    RECRUITER = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    RECRUITER_CODE = models.CharField(max_length=10, blank=True, null=True)
    CANDIDATE_STATUS = models.CharField(max_length=100, blank=True, null=True)
    CANDIDATE_STATUS_REMARKS = models.CharField(max_length=100, blank=True, null=True)
    EXPECTED_DOJ = models.DateField(blank=True, null=True)
    FINAL_DOJ = models.DateField(blank=True, null=True)
    DROP_OUT_REASON = models.CharField(max_length=255, blank=True, null=True)
    CV_APPROVE_DATE = models.DateField(blank=True, null=True)
    CV_APPROVE_BY = models.CharField(max_length=10, blank=True, null=True)
    CV_REJECT_BY = models.CharField(max_length=10, blank=True, null=True)
    SKILL_SET = models.CharField(max_length=255, blank=True, null=True)
    RESUME = models.FileField(upload_to=get_upload_path, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf'])])
    TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    CREATED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)
    MODIFIED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)
    LAST_MODIFIED = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    INTERVIEW_SCHEDULED = models.BooleanField(default=False)
    BILLING_STATUS = models.CharField(max_length=255, default="NOT APPLICABLE", null=True, blank=True)

    def __str__(self):
        if self.JOB_CODE:
            return str(self.JOB_CODE.CLIENT_CODE.CUSTOMER_CODE) + " - " + str(self.CANDIDATE_ID) + " - " + str(self.FIRST_NAME) + " " + str(self.LAST_NAME) if self.LAST_NAME else str(self.JOB_CODE.CLIENT_CODE.CUSTOMER_CODE) + " - " + str(self.CANDIDATE_ID) + " - " + str(self.FIRST_NAME)
        else:
            return str(self.CANDIDATE_ID) + " - " + str(self.FIRST_NAME) + " " + str(self.LAST_NAME) if self.LAST_NAME else str(self.CANDIDATE_ID) + " - " + str(self.FIRST_NAME)


class Interview(models.Model):
    INTERVIEW_ID = models.CharField(unique=True, max_length=10, null=True, blank=True, editable=False)
    CANDIDATE = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    INTERVIEW_TYPE = models.CharField(max_length=100, null=True, blank=True)
    INTERVIEW_ROUND = models.CharField(max_length=100, null=True, blank=True)
    INTERVIEW_LOCATION = models.CharField(max_length=255, null=True, blank=True)
    INTERVIEWER_NAME = models.ForeignKey(ClientSPOC, on_delete=models.CASCADE, null=True, blank=True)
    INTERVIEW_DATE = models.DateField(null=True, blank=True)
    INTERVIEW_TIME = models.TimeField(null=True, blank=True)
    INTERVIEW_STATUS = models.CharField(max_length=100, null=True, blank=True)
    INTERVIEW_COMMENTS = models.CharField(max_length=255, null=True, blank=True)
    REMARKS = models.CharField(max_length=255, null=True, blank=True)
    TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    CREATED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)
    MODIFIED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)
    LAST_MODIFIED = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.INTERVIEW_ID)


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)
