from django import forms
from django.forms import ModelForm
from apps.recruitment.models import *
from apps.recruitment.choices import *
from apps.employee.models import EducationList
from .choices import *


class OnlineCandidateForm(forms.ModelForm):
    DATE_OF_BIRTH = forms.DateField(required=True, label='DATE OF BIRTH',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    QUALIFICATION = forms.ModelChoiceField(required=True, label='QUALIFICATION',
                                                    queryset=EducationList.objects.values_list('name', flat=True),
                                                    to_field_name='name')
    MOBILE_NUMBER = forms.CharField(required=True, min_length=10, max_length=10, label='MOBILE NUMBER')
    ALTERNATE_PHONE = forms.CharField(required=False, min_length=8, max_length=30, label='ALTERNATE PHONE')
    PAN_NUMBER = forms.CharField(required=False, min_length=10, max_length=10, label='PAN NUMBER',
                                      widget=forms.TextInput(attrs={'pattern':'[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}'}))
    WORK_EXPERIENCE = forms.ChoiceField(required=True, choices=CHOICE_EXP, label='WORK EXPERIENCE (YEAR)')
    SOURCE = forms.ModelChoiceField(required=True, label='SOURCE',
                                    queryset=Source.objects.values_list('name', flat=True), to_field_name='name')

    class Meta:
        model = Candidate
        fields = ['FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'GENDER', 'PAN_NUMBER', 'SOURCE',
                  'EMAIL', 'SECONDARY_EMAIL', 'MOBILE_NUMBER', 'ALTERNATE_PHONE', 'QUALIFICATION', 'WORK_EXPERIENCE',
                  'LOCATION', 'RESUME']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_required = ['FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'GENDER', 'PAN_NUMBER', 'SOURCE',
                           'EMAIL', 'MOBILE_NUMBER', 'LOCATION', 'QUALIFICATION', 'WORK_EXPERIENCE', 'RESUME']
        for visible in self.visible_fields():
            if visible.name in fields_required:
                visible.field.widget.attrs['required'] = True
                visible.label = visible.label + " *"


class SearchApplicationForm(forms.ModelForm):
    SEARCH_BY = forms.ChoiceField(required=True, choices=CHOICE_SEARCH_BY_APPLICATIONS, label='SEARCH BY')
    SEARCH_TEXT = forms.CharField(required=True, label='SEARCH TEXT', widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Type for search'}))

    class Meta:
        model = Candidate
        fields = ['SEARCH_BY', 'SEARCH_TEXT']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
