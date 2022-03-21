from django.contrib import admin
from .models import UserHealthInfo, Group
# Register your models here.

admin.site.register(UserHealthInfo)
admin.site.register(Group)