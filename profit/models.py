'''Models for the Profit app'''
from datetime import datetime
from decimal import Decimal, DivisionByZero, InvalidOperation
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    '''Company a Job belongs to'''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Employee(models.Model):
    '''Employees are assigned to Jobs'''
    PAY_TYPES = (
        (0, 'Hourly'),
        (1, 'Salary'),
    )

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    pay_type = models.PositiveSmallIntegerField(default=PAY_TYPES[0][0],
                                                choices=PAY_TYPES)
    pay_rate = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

    def hourly_rate(self):
        '''The hourly rate of an employee'''
        if Employee.PAY_TYPES[self.pay_type][1] == 'Salary':
            return self.pay_rate / 40 / 52
        return self.pay_rate


class JobType(models.Model):
    '''Job Types are used to filter jobs'''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(models.Model):
    '''Jobs are the basis for calculating profitability'''
    name = models.CharField(max_length=40, db_index=True)
    revenue = models.DecimalField(max_digits=20, decimal_places=2)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    employee = models.ManyToManyField(Employee)
    date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def employees_str(self):
        '''Employees separated by a comma'''
        employees = [str(employee) for employee in self.employee.all()]
        return ', '.join(employees)

    def job_time(self):
        '''Job time in minutes'''
        clock_in = datetime.combine(self.date, self.clock_in)
        clock_out = datetime.combine(self.date, self.clock_out)
        delta = clock_out - clock_in
        return Decimal(delta.seconds / 60)

    def profitability(self):
        '''Profitability of a Job'''
        gross_revenue = self.revenue
        for employee in self.employee.all():
            employee_cost = employee.hourly_rate() * self.job_time() / 60
            gross_revenue = gross_revenue - employee_cost
        try:
            profitability = gross_revenue / self.job_time() * 60
        except (DivisionByZero, InvalidOperation):
            profitability = gross_revenue
        return format(profitability, '.2f')


class AlertSetting(models.Model):
    '''User or Company defined settings for Job Alerts'''
    ALERT_TYPES = (
        (0, 'Revenue'),
        (1, 'Start Time'),
        (2, 'End Time'),
        (3, 'Duration'),
        (4, 'Profitability'),
    )

    alert_filter = ArrayField(
        models.PositiveSmallIntegerField(
            choices=ALERT_TYPES, default=ALERT_TYPES[0][0], blank=False, null=False),
        size=5,
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    send_email = models.BooleanField(blank=False, null=False, default=False)
    email = ArrayField(models.EmailField())


class Alert(models.Model):
    '''Alerts are created for Jobs meeting criteria of AlertSettings'''
    created = models.DateTimeField(auto_now_add=True, editable=False)
    setting = models.ForeignKey(
        AlertSetting, on_delete=models.CASCADE, blank=False, null=False)
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, blank=False, null=False)
    read = models.BooleanField(blank=False, null=False, default=False)


class UserProfile(models.Model):
    '''User Profile for extending the User model'''
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE, db_index=True
    )
    companies = models.ManyToManyField(Company, verbose_name='Companies')

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        fullname = self.user.first_name + ' ' + self.user.last_name
        return fullname if fullname != ' ' else str(self.user)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''When a user is created, create a profile for them'''
    if created and not instance.profile:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    '''When a user is saved, save the profile as well'''
    instance.profile.save()
