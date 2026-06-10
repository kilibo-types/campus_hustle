from django.db import migrations
from django.contrib.auth.hashers import make_password

def seed_gigs(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('gigs', 'UserProfile')
    Gig = apps.get_model('gigs', 'Gig')
    
    # 1. Ensure we have at least one user to assign gigs to
    user, created = User.objects.get_or_create(
        username='campus_admin',
        defaults={
            'email': 'admin@campushustle.com',
            'password': make_password('AdminSecure123!'),
            'is_staff': True,
            'is_superuser': True
        }
    )
        
    # Ensure profile exists and has contact info so WhatsApp/phone links work
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.phone_number = '+256700000000'
    profile.whatsapp_number = '+256700000000'
    profile.bio = 'Official Campus Hustle Administrator profile.'
    profile.save()
    
    # 2. Add 7 gigs
    gigs_data = [
        {
            'title': 'Need urgent typing for 30-page lab report',
            'description': 'Looking for someone to type up my handwritten Chemistry lab report. Diagrams can be omitted, but all equations and tables must be accurately formatted. Deadline is this Friday.',
            'category': 'typing',
            'location': 'Makerere University Main Library',
            'price': 15000.00,
            'status': 'pending'
        },
        {
            'title': 'Mathematics (Calculus I) Tutor Needed',
            'description': 'Searching for an engineering or mathematics student to tutor me in Calculus I (limits, derivatives, and integration). Need 2 sessions a week, preferably in the evenings.',
            'category': 'tutoring',
            'location': 'University Hall Common Room',
            'price': 25000.00,
            'status': 'pending'
        },
        {
            'title': 'Logo & Poster Design for Campus Event',
            'description': 'We are organizing a student entrepreneurship expo next month and need a modern, eye-catching flyer design and a social media promo banner. Budget is fixed.',
            'category': 'design',
            'location': 'Remote / Online',
            'price': 40000.00,
            'status': 'pending'
        },
        {
            'title': 'Pick up package from Post Office / Courier',
            'description': 'Need someone to pick up a box of textbooks from the local courier office near campus and deliver it to Mitchell Hall room 14. Must be done tomorrow morning.',
            'category': 'errands',
            'location': 'Courier Office to Mitchell Hall',
            'price': 10000.00,
            'status': 'pending'
        },
        {
            'title': 'Data entry for Research Survey',
            'description': 'Help transcribe 150 paper survey questionnaires into an Excel spreadsheet. Straightforward work, should take about 3-4 hours if you type fast.',
            'category': 'typing',
            'location': 'Mary Stuart Hall / Remote',
            'price': 20000.00,
            'status': 'pending'
        },
        {
            'title': 'Python Programming tutoring for beginners',
            'description': 'I am struggling with my intro to computer science course. Need someone to explain loops, functions, and lists in Python, and help me with my assignments.',
            'category': 'tutoring',
            'location': 'Lumos Lab / CEDAT',
            'price': 30000.00,
            'status': 'pending'
        },
        {
            'title': 'UI Design Mockups for a mobile app idea',
            'description': 'Looking for a UI designer to create Figma wireframes and high-fidelity mockups (5 screens) for a campus food delivery app project.',
            'category': 'design',
            'location': 'Remote',
            'price': 50000.00,
            'status': 'pending'
        }
    ]
    
    for data in gigs_data:
        Gig.objects.get_or_create(
            title=data['title'],
            defaults={
                'poster': user,
                'description': data['description'],
                'category': data['category'],
                'location': data['location'],
                'price': data['price'],
                'status': data['status']
            }
        )

def remove_gigs(apps, schema_editor):
    Gig = apps.get_model('gigs', 'Gig')
    # Only delete the gigs we seeded
    titles = [
        'Need urgent typing for 30-page lab report',
        'Mathematics (Calculus I) Tutor Needed',
        'Logo & Poster Design for Campus Event',
        'Pick up package from Post Office / Courier',
        'Data entry for Research Survey',
        'Python Programming tutoring for beginners',
        'UI Design Mockups for a mobile app idea'
    ]
    Gig.objects.filter(title__in=titles).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0002_gig_location_gig_status_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_gigs, reverse_code=remove_gigs),
    ]
