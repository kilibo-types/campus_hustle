from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gigs.models import UserProfile

class Command(BaseCommand):
    help = 'Ensure every User has a UserProfile'

    def handle(self, *args, **options):
        User = get_user_model()
        created = 0
        for user in User.objects.all():
            profile = getattr(user, 'userprofile', None)
            if profile is None:
                UserProfile.objects.create(user=user)
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))
        if created == 0:
            self.stdout.write('All users already have profiles')
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {created} profiles'))
