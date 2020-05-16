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

    def hourly_rate(self, date):
        if self.pay_type is Employee.PAY_TYPES[0][0]:
            return self.pay_rate
        elif self.pay_type is Employee.PAY_TYPES[0][1]:
            return self.pay_rate / 40 / 52


class JobType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=100)
    revenue = models.DecimalField(max_digits=20, decimal_places=2)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    employee = models.ManyToManyField(Employee)

    def __str__(self):
        return self.name
