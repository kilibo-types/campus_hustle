from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import Gig, UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input'}))
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'input'}))
    whatsapp_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'textarea', 'rows': 4}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'whatsapp_number', 'bio', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.whatsapp_number = self.cleaned_data['whatsapp_number']
            profile.bio = self.cleaned_data['bio']
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input'}))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'whatsapp_number', 'bio']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'input'}),
            'bio': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
        }

    def save(self, user, commit=True):
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return profile


class GigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ['title', 'description', 'category', 'location', 'price', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'input'}),
            'location': forms.TextInput(attrs={'class': 'input'}),
            'price': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'input'}),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))