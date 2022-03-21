from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from user.models import User, UserGroup, UserProfile, UserFollowing

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(UserGroup)
admin.site.register(UserProfile)
admin.site.register(UserFollowing)
admin.site.unregister(Group)
# admin.site.register(Group)

