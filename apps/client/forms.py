from django import forms
from django.forms import ModelForm
from .models import *
from .choices import *


class ClientRegistrationForm(forms.ModelForm):
    CUSTOMER_START_DATE = forms.DateField(required=True, label='CUSTOMER START DATE',
                                      widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    CONTRACT_START_DATE = forms.DateField(required=True, label='CONTRACT START DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    CONTRACT_END_DATE = forms.DateField(required=True, label='CONTRACT END DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    PAN_NUMBER = forms.CharField(required=True, min_length=10, max_length=10, label='PAN NUMBER',
                                 widget=forms.TextInput(attrs={'pattern':'[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}'}))
    GSTIN_NUMBER = forms.CharField(required=True, min_length=15, max_length=15, label='GSTIN NUMBER')
    LOCATION_SERVE = forms.ChoiceField(required=True, label='LOCATION SERVE', choices=CHOICE_LOCATION_SERVE)

    class Meta:
        model = Client
        fields = ('CUSTOMER_NAME', 'CUSTOMER_START_DATE', 'CONTRACT_START_DATE', 'CONTRACT_END_DATE',
                  'MSMED_NUMBER', 'POTENTIAL_CUSTOMER', 'SKILL', 'LOCATION_SERVE', 'GSTIN_NUMBER',
                  'PAN_NUMBER')


class ClientAddressForm(forms.ModelForm):
    CORPORATE_ADDRESS = forms.CharField(required=True, max_length=255, label='CORPORATE ADDRESS')
    CORPORATE_CITY = forms.CharField(required=True, max_length=255, label='CORPORATE CITY')
    CORPORATE_STATE = forms.CharField(required=True, max_length=255, label='CORPORATE STATE')
    CORPORATE_PINCODE = forms.CharField(required=True, min_length=6, max_length=6, label='CORPORATE PINCODE')
    CORPORATE_COUNTRY = forms.ChoiceField(required=True, label='CORPORATE COUNTRY', choices=CHOICE_COUNTRY)
    # BILLING_COUNTRY = forms.ChoiceField(required=True, label='BILLING COUNTRY', choices=CHOICE_COUNTRY)

    class Meta:
        model = Client
        fields = ('CORPORATE_ADDRESS', 'CORPORATE_CITY', 'CORPORATE_STATE', 'CORPORATE_PINCODE', 'CORPORATE_COUNTRY',
                  'BOTH_ADDRESS_SAME', 'BILLING_ADDRESS', 'BILLING_CITY', 'BILLING_STATE', 'BILLING_PINCODE',
                  'BILLING_COUNTRY')


class ClientDocumentsForm(forms.ModelForm):

    class Meta:
        model = ClientDocuments
        fields = '__all__'
        exclude = ['UPLOADED_BY']


class AddNewSPOCForm(forms.ModelForm):

    class Meta:
        model = ClientSPOC
        fields = '__all__'
