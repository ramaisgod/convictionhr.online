from django.db import models
from .choices import *
from convictionhr_master.choices import *
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
import os


# Create your models here.
class Employee(models.Model):
    # My Profile
    EMPLOYEE_CODE = models.CharField(max_length=7, unique=True, blank=True, null=True, editable=False)
    EMPLOYEE_FULL_NAME = models.CharField(max_length=255, blank=True, null=True)
    FIRST_NAME = models.CharField(max_length=255)
    MIDDLE_NAME = models.CharField(max_length=255, blank=True, null=True)
    LAST_NAME = models.CharField(max_length=255, blank=True, null=True)
    FATHER_NAME = models.CharField(max_length=255, blank=True, null=True)
    DATE_OF_BIRTH = models.DateField(blank=True, null=True)
    PRESENT_ADDRESS = models.CharField(max_length=255, blank=True, null=True)
    PRESENT_CITY = models.CharField(max_length=255, blank=True, null=True)
    PRESENT_PIN = models.CharField(max_length=6, blank=True, null=True)
    GENDER = models.CharField(max_length=255, blank=True, null=True, choices=CHOICE_GENDER)
    AGE = models.PositiveIntegerField(default=0)
    EMERGENCY_CONTACT_NUMBER = models.CharField(max_length=30, blank=True, null=True)
    EMERGENCY_CONTACT_NAME = models.CharField(max_length=255, blank=True, null=True)
    BLOOD_GROUP = models.CharField(max_length=3, blank=True, null=True, choices=CHOICE_BLOODGROUP)
    PRIMARY_MOBILE_NO = models.CharField(max_length=10, blank=True, null=True)
    SECONDARY_MOBILE_NO = models.CharField(max_length=10, blank=True, null=True)
    MARITAL_STATUS = models.CharField(max_length=50, blank=True, null=True, choices=CHOICE_MARITAL)
    PERSONNEL_EMAIL = models.EmailField(max_length=255, blank=True, null=True)
    QUALIFICATION = models.CharField(max_length=255, blank=True, null=True)
    NATIONALITY = models.CharField(max_length=100, blank=True, null=True, choices=CHOICE_NATIONALITY)
    # Employee Details
    DATE_OF_JOINING = models.DateField(blank=True, null=True)
    DEPARTMENT = models.CharField(max_length=255, blank=True, null=True)
    DESIGNATION = models.CharField(max_length=255, blank=True, null=True)
    GRADE = models.CharField(max_length=20, blank=True, null=True)
    OPS_ROLE = models.CharField(max_length=255, blank=True, null=True)
    CATEGORY = models.CharField(max_length=255, blank=True, null=True, choices=CHOICE_SKILL)
    BRANCH = models.CharField(max_length=255, blank=True, null=True)
    LOCATION = models.CharField(max_length=255, blank=True, null=True)
    STATE = models.CharField(max_length=255, blank=True, null=True)
    EMPLOYEE_TYPE = models.CharField(max_length=50, blank=True, null=True, choices=CHOICE_EMP_TYPE)
    EMPLOYMENT_TYPE = models.CharField(max_length=50, blank=True, null=True)
    REPORTING_MANAGER_CODE = models.CharField(max_length=7, blank=True, null=True)
    REPORTING_MANAGER_NAME = models.CharField(max_length=100, blank=True, null=True)
    HR_MANAGER_CODE = models.CharField(max_length=7, blank=True, null=True)
    HR_MANAGER_NAME = models.CharField(max_length=100, blank=True, null=True)
    REFERENCE_NAME = models.CharField(max_length=255, blank=True, null=True)
    REFERENCE_CONTACT_NO = models.CharField(max_length=255, blank=True, null=True)
    REFERENCE_DESIGNATION = models.CharField(max_length=255, blank=True, null=True)
    OFFICIAL_EMAIL = models.EmailField(max_length=255, blank=True, null=True)
    DATE_OF_RESIGNATION = models.DateField(blank=True, null=True)
    RELIEVING_DATE = models.DateField(blank=True, null=True)
    DATE_OF_CONFIRMATION = models.DateField(blank=True, null=True)
    SWIPE_ATTENDANCE_NUMBER = models.CharField(max_length=20, blank=True, null=True)
    EMPLOYEE_STATUS = models.CharField(max_length=50, blank=True, null=True, choices=CHOICE_EMP_STATUS)
    SOURCE_OF_HIRE = models.CharField(max_length=255, blank=True, null=True)
    SUB_SOURCE = models.CharField(max_length=255, blank=True, null=True)
    # Last Employment Details
    TOTAL_EXPERIENCE = models.FloatField(blank=True, null=True)
    LAST_EMPLOYER_NAME = models.CharField(max_length=255, blank=True, null=True)
    LAST_EMPLOYER_START_DATE = models.DateField(blank=True, null=True)
    LAST_EMPLOYER_END_DATE = models.DateField(blank=True, null=True)
    LAST_EMPLOYER_CTC = models.FloatField(blank=True, null=True, default=0)
    # Bank Details
    AADHAAR_CARD_NO = models.CharField(max_length=12, blank=True, null=True)
    BANK_NAME = models.CharField(max_length=100, blank=True, null=True)
    IFSC_CODE = models.CharField(max_length=11, blank=True, null=True)
    BANK_BRANCH_NAME = models.CharField(max_length=100, blank=True, null=True)
    BANK_ACCOUNT_NO = models.CharField(max_length=20, blank=True, null=True)
    PAN_CARD_NUMBER = models.CharField(max_length=10, blank=True, null=True)
    TIMESTAMP = models.DateTimeField(auto_now_add=True, editable=False)
    CREATED_BY = models.CharField(max_length=10, null=True, blank=True)
    MODIFIED_BY = models.CharField(max_length=10, null=True, blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True, blank=True, editable=False)
    IS_USER_CREATED = models.BooleanField(default=False)

    def __str__(self):
        return str(self.EMPLOYEE_CODE) + " - " + str(self.FIRST_NAME) + " " + str(self.LAST_NAME) if self.LAST_NAME else str(self.EMPLOYEE_CODE) + " - " + str(self.FIRST_NAME)


def get_upload_path(instance, filename):
    return os.path.join('Employee//'+str(instance.EMPLOYEE_CODE.EMPLOYEE_CODE), filename)


class EmployeeDocuments(models.Model):
    EMPLOYEE_CODE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    DOCUMENT_TITLE = models.CharField(max_length=100)
    DOCUMENTS = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'xls', 'xlsx', 'pdf', 'zip', 'jpg', 'jpeg', 'png', 'ppt', 'pptx'])])
    UPLOAD_TIMESTAMP = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    UPLOADED_BY = models.CharField(max_length=10, null=True, blank=True, editable=False)

    def __str__(self):
        return str(self.EMPLOYEE_CODE)


class EducationList(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


# def get_upload_path(instance, filename):
#     return os.path.join('account/avatars/', now().date().strftime("%Y/%m/%d"), filename)
#
# class User(AbstractUser):
#     avatar = models.ImageField(blank=True, upload_to=get_upload_path)
