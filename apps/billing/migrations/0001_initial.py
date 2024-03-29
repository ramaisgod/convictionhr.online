# Generated by Django 3.0.10 on 2021-01-03 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recruitment', '0003_auto_20210103_1601'),
        ('client', '0002_auto_20201029_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PO_NUMBER', models.CharField(blank=True, max_length=255, null=True)),
                ('JOINING_LOCATION', models.CharField(blank=True, max_length=255, null=True)),
                ('PROCESS', models.CharField(blank=True, max_length=255, null=True)),
                ('SUB_PROCESS', models.CharField(blank=True, max_length=255, null=True)),
                ('DESIGNATION', models.CharField(blank=True, max_length=255, null=True)),
                ('DEPARTMENT', models.CharField(blank=True, max_length=255, null=True)),
                ('GRADE', models.CharField(blank=True, max_length=255, null=True)),
                ('INCENTIVE', models.CharField(blank=True, choices=[('', '---------'), ('YES', 'YES'), ('NO', 'NO')], max_length=255, null=True)),
                ('INCENTIVE_CODE', models.CharField(blank=True, max_length=255, null=True)),
                ('OFFERED_CTC', models.FloatField(blank=True, null=True)),
                ('BILLING_CTC', models.FloatField(blank=True, null=True)),
                ('BILLING_CHARGES_PERCENTAGE', models.FloatField(blank=True, null=True)),
                ('HIRING_COST', models.FloatField(blank=True, null=True)),
                ('CGST', models.FloatField(blank=True, null=True)),
                ('SGST', models.FloatField(blank=True, null=True)),
                ('IGST', models.FloatField(blank=True, null=True)),
                ('INVOICE_AMOUNT', models.FloatField(blank=True, null=True)),
                ('INVOICE_NUMBER', models.CharField(blank=True, max_length=255, null=True)),
                ('INVOICE_DATE', models.DateField(blank=True, null=True)),
                ('INVOICE_SENT_TO_CUSTOMER', models.CharField(blank=True, max_length=255, null=True)),
                ('PHYSICAL_OR_SOFT_COPY', models.CharField(blank=True, max_length=255, null=True)),
                ('INVOICE_STATUS', models.CharField(blank=True, max_length=255, null=True)),
                ('PAID_ON', models.DateField(blank=True, null=True)),
                ('LWD', models.CharField(blank=True, max_length=255, null=True)),
                ('UNIQUE_REF_NO', models.CharField(blank=True, max_length=255, null=True)),
                ('GST_NUMBER', models.CharField(blank=True, max_length=255, null=True)),
                ('PAN_NUMBER', models.CharField(blank=True, max_length=255, null=True)),
                ('EMAIL_ID', models.CharField(blank=True, max_length=255, null=True)),
                ('MOBILE_NO', models.CharField(blank=True, max_length=255, null=True)),
                ('BILLING_DETAILS_RECEIVED_ON', models.CharField(blank=True, max_length=255, null=True)),
                ('REMARKS', models.CharField(blank=True, max_length=255, null=True)),
                ('RAISED_BY', models.CharField(blank=True, max_length=255, null=True)),
                ('CREDIT_NOTE_NO', models.CharField(blank=True, max_length=255, null=True)),
                ('CREDIT_NOTE_DATE', models.DateField(blank=True, null=True)),
                ('TIMESTAMP', models.DateTimeField(auto_now_add=True, null=True)),
                ('MODIFIED_BY', models.CharField(blank=True, editable=False, max_length=10, null=True)),
                ('LAST_MODIFIED', models.DateTimeField(auto_now=True, null=True)),
                ('CANDIDATE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.Candidate')),
                ('CUSTOMER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
            ],
        ),
    ]
