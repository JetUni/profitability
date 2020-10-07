'''Admin for the Profit app'''
from django.contrib import admin

from profit.models import Company, Employee, Job, JobType


admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(JobType)
