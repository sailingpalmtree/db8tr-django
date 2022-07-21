from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
# from django.contrib.auth.models import Group

# Unregistering the Group option from the models:
# https://realpython.com/django-social-network-1/#step-1-set-up-the-base-project
# admin.site.unregister(Group)

# Register your models here.

# Removed since they are shown inline with the users.
# admin.site.register(DebateQueue)
# admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)