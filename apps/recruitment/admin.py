from django.contrib import admin
from .models import *


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "ASSIGNED_SPOC":
            kwargs["queryset"] = Employee.objects.filter(IS_USER_CREATED=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register((Candidate, Interview, SubSkill, Source))
