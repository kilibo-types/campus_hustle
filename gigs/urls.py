from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_page'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('gigs/create/', views.gig_create, name='gig_create'),
    path('gigs/<int:pk>/', views.gig_detail, name='gig_detail'),
    path('gigs/<int:pk>/edit/', views.gig_edit, name='gig_edit'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
