'''Admin for the Profit app'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from profit.models import Company, Employee, Job, JobType, UserProfile


class UserProfileInline(admin.StackedInline):
    '''User Profile Admin for adding to Custom User Admin'''
    model = UserProfile
    can_delete = False
    verbose_name = 'User Profile'
    verbose_name_plural = 'User Profiles'


class UserAdmin(BaseUserAdmin):
    '''Custom User Admin'''
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(JobType)
