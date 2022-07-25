from django.contrib import admin
from .models import User


admin.AdminSite.site_title = "Admin Panel"
admin.AdminSite.site_header = "ConvictionHR"
admin.AdminSite.index_title = "ConvictionHR Administrator"
# Register your models here.
admin.site.register(User)
