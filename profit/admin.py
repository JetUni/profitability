from django.contrib import admin
from .models import (Employee, Job, JobType)


admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(JobType)
