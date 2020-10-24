from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from profit.models import Company


class Command(BaseCommand):
    help = 'Add all companies to superadmin users'

    def handle(self, *args, **options):
        '''Add all companies to super admins'''
        companies = Company.objects.all()
        for user in User.objects.filter(is_staff=True):
            for company in companies:
                user.profile.companies.add(company)
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully added companies to "%s"' % user))
        self.stdout.write(self.style.SUCCESS('OK'))
