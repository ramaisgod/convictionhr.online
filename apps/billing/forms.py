from django import forms
from .models import *


class NewInvoiceForm(forms.ModelForm):
    CREDIT_NOTE_DATE = forms.DateField(required=True, label='CREDIT NOTE DATE',
                                    widget=forms.DateInput(attrs={"class": "flatpickr bg-white", "placeholder": "YYYY-MM-DD"}))
    PAN_NUMBER = forms.CharField(required=True, min_length=10, max_length=10, label='PAN NUMBER',
                                      widget=forms.TextInput(attrs={'pattern':'[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}'}))
    MOBILE_NO = forms.CharField(required=True, min_length=10, max_length=10, label='MOBILE NUMBER')
    GST_NUMBER = forms.CharField(required=True, min_length=15, max_length=15, label='GST NUMBER')

    class Meta:
        model = BillingTracker
        fields = ('PO_NUMBER', 'JOINING_LOCATION', 'PROCESS', 'SUB_PROCESS', 'DESIGNATION', 'DEPARTMENT', 'GRADE',
                  'INCENTIVE', 'INCENTIVE_CODE', 'OFFERED_CTC', 'BILLING_CTC', 'BILLING_CHARGES_PERCENTAGE',
                  'HIRING_COST', 'CGST', 'SGST', 'IGST', 'INVOICE_AMOUNT', 'UNIQUE_REF_NO', 'GST_NUMBER', 'PAN_NUMBER', 
                  'EMAIL_ID', 'MOBILE_NO', 'REMARKS', 'CREDIT_NOTE_NO', 'CREDIT_NOTE_DATE')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ASSIGNED_SPOC'].queryset = Employee.objects.filter(IS_USER_CREATED=True)
        for visible in self.visible_fields():
            visible.field.widget.attrs['required'] = True
            # visible.field.widget.attrs['class'] = 'form-control'
