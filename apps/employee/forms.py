from django import forms
from django.forms import ModelForm
from .models import *
from .choices import *
from convictionhr_master.choices import *


class EmployeeRegistrationForm(forms.ModelForm):
    FATHER_NAME = forms.CharField(required=True, label='FATHER NAME')
    DATE_OF_BIRTH = forms.DateField(required=True, label='DATE OF BIRTH',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    GENDER = forms.ChoiceField(required=True, label='GENDER', choices=CHOICE_GENDER)
    QUALIFICATION = forms.ModelChoiceField(required=True, queryset=EducationList.objects.values_list('name', flat=True).distinct(),
                                           to_field_name='name', label='QUALIFICATION')
    PERSONNEL_EMAIL = forms.EmailField(required=True, label='PERSONNEL EMAIL')
    PRIMARY_MOBILE_NO = forms.CharField(required=True, min_length=10, max_length=10, label='PRIMARY MOBILE NO')
    SECONDARY_MOBILE_NO = forms.CharField(required=False, min_length=10, max_length=10, label='SECONDARY MOBILE NO')
    NATIONALITY = forms.ChoiceField(required=True, label='NATIONALITY', choices=CHOICE_NATIONALITY)

    class Meta:
        model = Employee
        fields = ('FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FATHER_NAME',
                  'DATE_OF_BIRTH', 'PRESENT_ADDRESS', 'PRESENT_CITY', 'PRESENT_PIN', 'GENDER',
                  'EMERGENCY_CONTACT_NUMBER', 'EMERGENCY_CONTACT_NAME', 'BLOOD_GROUP', 'PRIMARY_MOBILE_NO',
                  'SECONDARY_MOBILE_NO', 'MARITAL_STATUS', 'PERSONNEL_EMAIL', 'QUALIFICATION', 'NATIONALITY')


class WorkDetailsForm(forms.ModelForm):
    DATE_OF_JOINING = forms.DateField(required=True, label='DATE OF JOINING',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    EMPLOYEE_TYPE = forms.ChoiceField(required=True, label='EMPLOYEE TYPE', choices=CHOICE_EMP_TYPE)
    EMPLOYMENT_TYPE = forms.ChoiceField(required=True, label='EMPLOYMENT TYPE', choices=CHOICE_EMPLOYMENT)
    OPS_ROLE = forms.ChoiceField(required=True, label='OPS ROLE', choices=CHOICE_ROLE)
    CATEGORY = forms.ChoiceField(required=True, label='CATEGORY', choices=CHOICE_SKILL)
    BRANCH = forms.ChoiceField(required=True, label='BRANCH', choices=CHOICE_BRANCH)
    LOCATION = forms.ChoiceField(required=True, label='LOCATION', choices=CHOICE_LOCATION)
    STATE = forms.ChoiceField(required=True, label='STATE', choices=CHOICE_STATE)
    SOURCE_OF_HIRE = forms.ChoiceField(required=True, label='SOURCE OF HIRE', choices=CHOICE_SOURCE_HIRE)
    OFFICIAL_EMAIL = forms.EmailField(required=True, label='OFFICIAL EMAIL')
    REPORTING_MANAGER_CODE = forms.CharField(required=True, min_length=7, max_length=7, label='REPORTING MANAGER CODE')
    REPORTING_MANAGER_NAME = forms.CharField(required=True, label='REPORTING MANAGER NAME',
                                    widget=forms.TextInput(attrs={"readonly": "true"}))
    HR_MANAGER_CODE = forms.CharField(required=True, min_length=7, max_length=7, label='HR MANAGER CODE')
    HR_MANAGER_NAME = forms.CharField(required=True, label='HR MANAGER NAME',
                                    widget=forms.TextInput(attrs={"readonly": "true"}))

    class Meta:
        model = Employee
        fields = ('DATE_OF_JOINING', 'DEPARTMENT', 'DESIGNATION', 'GRADE', 'OPS_ROLE', 'CATEGORY', 'BRANCH', 'LOCATION',
                  'STATE', 'EMPLOYEE_TYPE', 'EMPLOYMENT_TYPE', 'OFFICIAL_EMAIL', 'REPORTING_MANAGER_CODE', 'REPORTING_MANAGER_NAME',
                  'REFERENCE_NAME', 'REFERENCE_CONTACT_NO', 'REFERENCE_DESIGNATION', 'SWIPE_ATTENDANCE_NUMBER', 'HR_MANAGER_CODE',
                  'HR_MANAGER_NAME', 'SOURCE_OF_HIRE', 'SUB_SOURCE')


class LastEmploymentForm(ModelForm):
    LAST_EMPLOYER_NAME = forms.CharField(required=True, label='LAST EMPLOYER NAME')
    LAST_EMPLOYER_START_DATE = forms.DateField(required=True, label='LAST EMPLOYER START DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    LAST_EMPLOYER_END_DATE = forms.DateField(required=True, label='LAST EMPLOYER END DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))

    class Meta:
        model = Employee
        fields = ('TOTAL_EXPERIENCE', 'LAST_EMPLOYER_NAME', 'LAST_EMPLOYER_START_DATE', 'LAST_EMPLOYER_END_DATE',
                  'LAST_EMPLOYER_CTC')


class BankDetailsForm(ModelForm):
    AADHAAR_CARD_NO = forms.CharField(min_length=12, max_length=12, label='AADHAAR CARD NO')
    PAN_CARD_NUMBER = forms.CharField(min_length=10, max_length=10, label='PAN CARD NUMBER',
                                      widget=forms.TextInput(attrs={'pattern':'[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}'}))
    IFSC_CODE = forms.CharField(min_length=11, max_length=11, label='IFSC CODE')

    class Meta:
        model = Employee
        fields = ('AADHAAR_CARD_NO', 'BANK_NAME', 'IFSC_CODE', 'BANK_BRANCH_NAME', 'BANK_ACCOUNT_NO', 'PAN_CARD_NUMBER')

    def __init__(self, *args, **kwargs):
        super(BankDetailsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['required'] = True


class EmployeeDocumentsForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocuments
        fields = '__all__'
        exclude = ['UPLOADED_BY']
