from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
	phone_number = models.CharField(max_length=20, blank=True)
	whatsapp_number = models.CharField(max_length=20, blank=True)
	bio = models.TextField(blank=True)
	email = models.EmailField(blank=True)

	def __str__(self):
		return f'{self.user.username} profile'


class Gig(models.Model):
	TYPING = 'typing'
	TUTORING = 'tutoring'
	DESIGN = 'design'
	ERRANDS = 'errands'
	OTHER = 'other'

	PENDING = 'pending'
	ACCEPTED = 'accepted'
	COMPLETED = 'completed'

	CATEGORY_CHOICES = [
		(TYPING, 'Typing Assignments'),
		(TUTORING, 'Tutoring'),
		(DESIGN, 'Design Work'),
		(ERRANDS, 'Errands'),
		(OTHER, 'Other'),
	]

	STATUS_CHOICES = [
		(PENDING, 'Pending'),
		(ACCEPTED, 'Accepted'),
		(COMPLETED, 'Completed'),
	]

	poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
	title = models.CharField(max_length=180)
	description = models.TextField()
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTHER)
	location = models.CharField(max_length=180, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
	created_at = models.DateTimeField(auto_now_add=True)
	is_completed = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.title} ({self.poster.username})'

	@property
	def whatsapp_link(self):
		profile = getattr(self.poster, 'userprofile', None)
		if profile and profile.whatsapp_number:
			number = ''.join(ch for ch in profile.whatsapp_number if ch.isdigit())
			return f'https://wa.me/{number}'
		return None

	@property
	def phone_link(self):
		profile = getattr(self.poster, 'userprofile', None)
		if profile and profile.phone_number:
			number = ''.join(ch for ch in profile.phone_number if ch.isdigit())
			return f'tel:{number}'
		return None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
