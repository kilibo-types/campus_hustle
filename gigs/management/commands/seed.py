from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gigs.models import Gig, UserProfile

from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Seed the database with demo users and gigs'

    def handle(self, *args, **options):
        User = get_user_model()
        users_data = [
            {'username': 'alice', 'email': 'alice@example.com', 'password': 'password123', 'phone': '+256772000001', 'wa': '+256772000001'},
            {'username': 'bob', 'email': 'bob@example.com', 'password': 'password123', 'phone': '+256772000002', 'wa': '+256772000002'},
        ]
        created_users = []
        for u in users_data:
            if not User.objects.filter(username=u['username']).exists():
                user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'])
                profile = getattr(user, 'userprofile', None)
                if profile is None:
                    profile = UserProfile.objects.create(user=user)
                profile.phone_number = u['phone']
                profile.whatsapp_number = u['wa']
                profile.save()
                created_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user {user.username}'))
            else:
                user = User.objects.get(username=u['username'])
                created_users.append(user)
                self.stdout.write(f'User exists: {user.username}')

        if not Gig.objects.exists():
            gigs = [
                {'poster': created_users[0], 'title': 'Type up assignment (2 pages)', 'description': 'Need someone to type and format two pages of notes.', 'category': Gig.TYPING, 'price': 10000},
                {'poster': created_users[1], 'title': 'Math tutoring session', 'description': 'Tutoring for first-year calculus, 2 hours.', 'category': Gig.TUTORING, 'price': 20000},
                {'poster': created_users[0], 'title': 'Logo design', 'description': 'Design a simple logo for a student group.', 'category': Gig.DESIGN, 'price': 30000},
            ]
            for g in gigs:
                Gig.objects.create(**g)
            self.stdout.write(self.style.SUCCESS('Created demo gigs'))
        else:
            self.stdout.write('Gigs already present; skipping gig creation')

        self.stdout.write(self.style.SUCCESS('Seeding complete'))
