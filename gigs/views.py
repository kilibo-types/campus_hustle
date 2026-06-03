from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import CustomLoginForm, GigForm, ProfileForm, UserRegistrationForm
from .models import Gig


@login_required
def dashboard(request):
	profile = getattr(request.user, 'userprofile', None)
	pending_gigs = request.user.gigs.filter(status=Gig.PENDING)
	accepted_gigs = request.user.gigs.filter(status=Gig.ACCEPTED)
	completed_gigs = request.user.gigs.filter(status=Gig.COMPLETED)
	context = {
		'profile': profile,
		'pending_gigs': pending_gigs,
		'accepted_gigs': accepted_gigs,
		'completed_gigs': completed_gigs,
	}
	return render(request, 'gigs/dashboard.html', context)


def marketplace(request):
	"""Public marketplace view showing active gigs to apply for."""
	category = request.GET.get('category', '')
	query = request.GET.get('q', '')
	gigs = Gig.objects.filter(status=Gig.PENDING)
	if category:
		gigs = gigs.filter(category=category)
	if query:
		gigs = gigs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
	context = {
		'gigs': gigs,
		'categories': Gig.CATEGORY_CHOICES,
		'active_category': category,
		'query': query,
	}
	return render(request, 'gigs/marketplace.html', context)


def gig_detail(request, pk):
	gig = get_object_or_404(Gig, pk=pk)
	context = {
		'gig': gig,
		'whatsapp_link': gig.whatsapp_link,
		'phone_link': gig.phone_link,
	}
	return render(request, 'gigs/gig_detail.html', context)


@login_required
def gig_create(request):
	if request.method == 'POST':
		form = GigForm(request.POST)
		if form.is_valid():
			gig = form.save(commit=False)
			gig.poster = request.user
			gig.save()
			messages.success(request, 'Your gig has been posted successfully.')
			return redirect('gig_detail', pk=gig.pk)
	else:
		form = GigForm()
	return render(request, 'gigs/gig_form.html', {'form': form})


@login_required
def gig_edit(request, pk):
	gig = get_object_or_404(Gig, pk=pk, poster=request.user)
	if request.method == 'POST':
		form = GigForm(request.POST, instance=gig)
		if form.is_valid():
			form.save()
			messages.success(request, 'Gig updated successfully.')
			return redirect('dashboard')
	else:
		form = GigForm(instance=gig)
	return render(request, 'gigs/gig_form.html', {'form': form, 'edit_mode': True})


@login_required
def profile_view(request):
	profile = getattr(request.user, 'userprofile', None)
	return render(request, 'gigs/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
	profile = getattr(request.user, 'userprofile', None)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save(request.user)
			messages.success(request, 'Profile updated successfully.')
			return redirect('profile')
	else:
		initial = {
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'email': request.user.email,
		}
		form = ProfileForm(instance=profile, initial=initial)
	return render(request, 'gigs/profile_edit.html', {'form': form})


def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Registration successful. Welcome to Campus Hustle!')
			return redirect('dashboard')
	else:
		form = UserRegistrationForm()
	return render(request, 'gigs/register.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		form = CustomLoginForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(
				request,
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'],
			)
			if user is not None:
				login(request, user)
				messages.success(request, 'You are now logged in.')
				return redirect('dashboard')
	else:
		form = CustomLoginForm()
	return render(request, 'gigs/login.html', {'form': form})


def logout_view(request):
	logout(request)
	messages.success(request, 'You have been logged out.')
	return redirect('login')
