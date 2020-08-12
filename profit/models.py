from decimal import Decimal, DivisionByZero
from django.db import models


class Employee(models.Model):
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
        if Employee.PAY_TYPES[self.pay_type][1] == 'Salary':
            return self.pay_rate / 40 / 52
        return self.pay_rate


class JobType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=100)
    revenue = models.DecimalField(max_digits=20, decimal_places=2)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    employee = models.ManyToManyField(Employee)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()

    def __str__(self):
        return self.name

    def employees_str(self):
        employees = [str(employee) for employee in self.employee.all()]
        return ', '.join(employees)

    def job_time(self):
        delta = self.clock_out - self.clock_in
        return Decimal(delta.seconds / 60)

    def profitability(self):
        gross_revenue = self.revenue
        for employee in self.employee.all():
            employee_cost = employee.hourly_rate() * self.job_time() / 60
            gross_revenue = gross_revenue - employee_cost
        try:
            profitability = gross_revenue / self.job_time() * 60
        except (DivisionByZero):
            profitability = gross_revenue
        return format(profitability, '.2f')
