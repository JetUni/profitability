from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from profit.models import UserProfile


class Command(BaseCommand):
    help = 'Add a UserProfile to all users without one'

    def handle(self, *args, **options):
        '''Add a UserProfile to all users without one'''
        for user in User.objects.filter(profile__isnull=True):
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS('Successfully created UserProfile for "%s"' % user))
        self.stdout.write(self.style.SUCCESS('OK'))
