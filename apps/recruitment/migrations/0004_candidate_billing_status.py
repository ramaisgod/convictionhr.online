# Generated by Django 3.0.10 on 2021-01-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0003_auto_20210103_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='BILLING_STATUS',
            field=models.CharField(blank=True, default='Pending', max_length=255, null=True),
        ),
    ]
