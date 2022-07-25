from django import forms
from .models import *
from apps.employee.models import EducationList


class NewCVForm(forms.ModelForm):
    DATE_OF_BIRTH = forms.DateField(required=True, label='DATE OF BIRTH',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    QUALIFICATION = forms.ModelChoiceField(required=True, label='QUALIFICATION',
                                                    queryset=EducationList.objects.values_list('name', flat=True),
                                                    to_field_name='name')
    MOBILE_NUMBER = forms.CharField(required=True, min_length=10, max_length=10, label='MOBILE NUMBER')
    ALTERNATE_PHONE = forms.CharField(required=False, min_length=8, max_length=30, label='ALTERNATE PHONE')
    PAN_NUMBER = forms.CharField(min_length=10, max_length=10, label='PAN NUMBER',
                                      widget=forms.TextInput(attrs={'pattern':'[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}'}))

    class Meta:
        model = CVRepo
        fields = ['FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'GENDER', 'PAN_NUMBER', 'MOBILE_NUMBER', 'ALTERNATE_PHONE',
                  'EMAIL', 'SECONDARY_EMAIL', 'QUALIFICATION', 'WORK_EXPERIENCE', 'CURRENT_LOCATION', 'SKILLS',
                  'SOURCE', 'SUB_SOURCE', 'REMARKS', 'RESUME']

    def __init__(self, *args, **kwargs):
        super(NewCVForm, self).__init__(*args, **kwargs)
        fields_required = ['FIRST_NAME', 'DATE_OF_BIRTH', 'GENDER', 'MOBILE_NUMBER', 'EMAIL', 'CURRENT_LOCATION',
                           'SOURCE', 'SUB_SOURCE', 'RESUME']
        for visible in self.visible_fields():
            if visible.name in fields_required:
                visible.field.widget.attrs['required'] = True


class SearchCVForm(forms.ModelForm):
    SEARCH_BY = forms.ChoiceField(required=True, choices=CHOICE_SEARCH_BY, label='SEARCH BY')
    SEARCH_TEXT = forms.CharField(required=False, label='SEARCH TEXT')
    QUALIFICATION = forms.ModelChoiceField(required=False, label='QUALIFICATION',
                                                    queryset=EducationList.objects.values_list('name', flat=True),
                                                    to_field_name='name')
    PAN_NUMBER = forms.CharField(required=False, min_length=10, max_length=10, label='PAN NUMBER',
                                      widget=forms.TextInput(attrs={'pattern':'[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}'}))

    class Meta:
        model = CVRepo
        fields = ['SEARCH_BY', 'SEARCH_TEXT', 'GENDER', 'PAN_NUMBER', 'EMAIL', 'QUALIFICATION']

    def __init__(self, *args, **kwargs):
        super(SearchCVForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class AutoUploadCVForm(forms.ModelForm):
    RESUME = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file form-control'}))
    MOBILE_NUMBER = forms.CharField(required=False, min_length=10, max_length=10, label='MOBILE NUMBER')

    class Meta:
        model = CVRepo
        fields = ['RESUME', 'FIRST_NAME', 'LAST_NAME', 'GENDER', 'MOBILE_NUMBER', 'EMAIL', 'SKILLS', 'REMARKS']

