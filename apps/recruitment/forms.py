from django import forms
from django.forms import ModelForm
from .models import *
from .choices import *
from apps.employee.models import EducationList


class JobForm(forms.ModelForm):
    JOB_START_DATE = forms.DateField(required=True, label='JOB START DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    TARGET_DATE = forms.DateField(required=True, label='TARGET DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    # SKILL = forms.ChoiceField(required=True, label='SKILL', choices=CHOICE_SKILL)
    SUB_SKILL = forms.ModelChoiceField(required=True, label='SUB SKILL',
                                       queryset=SubSkill.objects.values_list('name', flat=True), to_field_name='name')
    PRIORITY_TYPE = forms.ChoiceField(required=True, label='PRIORITY TYPE', choices=CHOICE_PRIORITY)
    NUMBER_OF_POSITIONS = forms.CharField(required=True, label='NUMBER OF POSITIONS',
                                          widget=forms.NumberInput(attrs={'min': '1'}))
    REQUIRED_QUALIFICATION = forms.ModelChoiceField(required=True, label='REQUIRED QUALIFICATION',
                                                    queryset=EducationList.objects.values_list('name', flat=True),
                                                    to_field_name='name')

    class Meta:
        model = Job
        fields = ('CLIENT_CODE', 'JOB_TITLE', 'NUMBER_OF_POSITIONS', 'JOB_START_DATE', 'TARGET_DATE', 'JOB_TYPE',
                  'SKILL', 'SUB_SKILL', 'JOB_SHIFT', 'ASSIGNED_SPOC', 'LINE_OF_BUSINESS', 'PRIORITY_TYPE', 'WORK_EXPERIENCE', 'JOB_LOCATION',
                  'REQUIRED_QUALIFICATION', 'JOB_DESCRIPTION')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        fields_not_required = ['JOB_TYPE',]
        self.fields['ASSIGNED_SPOC'].queryset = Employee.objects.filter(IS_USER_CREATED=True)
        for visible in self.visible_fields():
            if visible.name not in fields_not_required:
                visible.field.widget.attrs['required'] = True


class NewCandidateForm(forms.ModelForm):
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
    SOURCE = forms.ModelChoiceField(required=True, label='SOURCE', queryset=Source.objects.values_list('name', flat=True), to_field_name='name')

    class Meta:
        model = Candidate
        fields = ['JOB_CODE', 'FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'GENDER', 'PAN_NUMBER', 'SOURCE', 'SUB_SOURCE',
                  'EMAIL', 'SECONDARY_EMAIL', 'MOBILE_NUMBER', 'ALTERNATE_PHONE', 'QUALIFICATION', 'WORK_EXPERIENCE',
                  'LOCATION', 'RESUME']

    def __init__(self, *args, **kwargs):
        super(NewCandidateForm, self).__init__(*args, **kwargs)
        fields_required = ['JOB_CODE', 'FIRST_NAME', 'DATE_OF_BIRTH', 'GENDER', 'SOURCE', 'SUB_SOURCE', 'EMAIL',
                           'MOBILE_NUMBER', 'LOCATION', 'QUALIFICATION', 'WORK_EXPERIENCE', 'RESUME']
        for visible in self.visible_fields():
            if visible.name in fields_required:
                visible.field.widget.attrs['required'] = True


class InterviewForm(forms.ModelForm):
    INTERVIEW_DATE = forms.DateField(required=True, label='INTERVIEW DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    INTERVIEW_TYPE = forms.ChoiceField(choices=CHOICE_INTERVIEW_TYPE, label='INTERVIEW TYPE')
    INTERVIEW_ROUND = forms.ChoiceField(choices=CHOICE_INTERVIEW_ROUND, label='INTERVIEW ROUND')
    INTERVIEW_TIME = forms.TimeField(label='INTERVIEW TIME', widget=forms.TimeInput(attrs={"class": "timepicker bg-white", 'placeholder': 'HH:MM  (24hrs format)'}))

    class Meta:
        model = Interview
        fields = '__all__'
        exclude = ['INTERVIEW_STATUS', 'INTERVIEW_COMMENTS']

    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        fields_not_required = ['REMARKS']
        for visible in self.visible_fields():
            if visible.name not in fields_not_required:
                visible.field.widget.attrs['required'] = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['INTERVIEWER_NAME'].queryset = ClientSPOC.objects.none()


class InterviewStatusForm(forms.ModelForm):
    INTERVIEW_ROUND = forms.ChoiceField(choices=CHOICE_INTERVIEW_ROUND, label='INTERVIEW ROUND')
    INTERVIEW_STATUS = forms.ChoiceField(choices=CHOICE_INTERVIEW_STATUS, label='INTERVIEW STATUS')
    CANDIDATE_STATUS = forms.CharField(label='CANDIDATE STATUS', widget=forms.Select())
    INTERVIEW_COMMENTS = forms.CharField(required=False, max_length=255, label='COMMENTS')

    class Meta:
        model = Interview
        fields = ['INTERVIEW_ROUND', 'INTERVIEW_STATUS', 'CANDIDATE_STATUS', 'INTERVIEW_COMMENTS']

    def __init__(self, *args, **kwargs):
        super(InterviewStatusForm, self).__init__(*args, **kwargs)
        fields_required = ['INTERVIEW_ROUND', 'INTERVIEW_STATUS', 'CANDIDATE_STATUS']
        for visible in self.visible_fields():
            if visible.name in fields_required:
                visible.field.widget.attrs['required'] = True


class SearchCandidateForm(forms.ModelForm):
    SEARCH_BY = forms.ChoiceField(required=True, choices=CHOICE_SEARCH_BY_CANDIDATE, label='SEARCH BY')
    SEARCH_TEXT = forms.CharField(required=True, label='SEARCH TEXT', widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Type for search'}))

    class Meta:
        model = Candidate
        fields = ['SEARCH_BY', 'SEARCH_TEXT']

    def __init__(self, *args, **kwargs):
        super(SearchCandidateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class SearchInterviewForm(forms.ModelForm):
    SEARCH_BY = forms.ChoiceField(required=True, choices=CHOICE_SEARCH_BY_INTERVIEW, label='SEARCH BY')
    SEARCH_TEXT = forms.CharField(required=True, label='SEARCH TEXT', widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Type for search'}))

    class Meta:
        model = Candidate
        fields = ['SEARCH_BY', 'SEARCH_TEXT']

    def __init__(self, *args, **kwargs):
        super(SearchInterviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class SearchJobForm(forms.ModelForm):
    SEARCH_BY = forms.ChoiceField(required=True, choices=CHOICE_SEARCH_BY_JOB, label='SEARCH BY')
    SEARCH_TEXT = forms.CharField(required=True, label='SEARCH TEXT', widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Type for search'}))

    class Meta:
        model = Candidate
        fields = ['SEARCH_BY', 'SEARCH_TEXT']

    def __init__(self, *args, **kwargs):
        super(SearchJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"


class SearchAssignedJobForm(forms.ModelForm):
    SEARCH_BY = forms.ChoiceField(required=True, choices=CHOICE_SEARCH_BY_ASSIGNED_JOB, label='SEARCH BY')
    SEARCH_TEXT = forms.CharField(required=True, label='SEARCH TEXT', widget=forms.TextInput(attrs={'type': 'search', 'placeholder': 'Type for search'}))

    class Meta:
        model = Candidate
        fields = ['SEARCH_BY', 'SEARCH_TEXT']

    def __init__(self, *args, **kwargs):
        super(SearchAssignedJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
