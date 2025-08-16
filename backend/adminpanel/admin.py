from django.contrib import admin
from .models import SystemSetting, AdminLog

admin.site.register(SystemSetting)
admin.site.register(AdminLog)