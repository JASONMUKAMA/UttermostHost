from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import (
    aboutpage, electronicsolutions, ictsolutions, eduSolutions,
    mediasolutions, consultancysolutions, industries, innovationcenter,
    careers, investorrelations, contact_us, job_list, job_detail,
    UserProfileCreateView, UserProfileUpdateView, UserProfileListView,
    activate, search_view, download_cheatsheet
)

urlpatterns = [
    # General Pages
    path('', views.index, name='index'),
    path('aboutus/', aboutpage, name='aboutpage'),
    path('electronicsolutions/', electronicsolutions, name='electronicsolutions'),
    path('ictsolutions/', ictsolutions, name='ictsolutions'),
    path('eduSolutions/', eduSolutions, name='eduSolutions'),
    path('mediasolutions/', mediasolutions, name='mediasolutions'),
    path('consultancysolutions/', consultancysolutions, name='consultancysolutions'),
    path('industries/', industries, name='industries'),
    path('innovationcenter/', innovationcenter, name='innovationcenter'),
    path('careers/', careers, name='careers'),
    path('investorrelations/', investorrelations, name='investorrelations'),
    path('contact_us/', contact_us, name='contact_us'),

    # Applications
    path('Applications/', views.PersonListView.as_view(), name='person_changelist'),
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

    # Jobs
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:category_id>/', job_detail, name='job_detail'),

    # User Profiles
    path('profiles/create/', UserProfileCreateView.as_view(), name='profile-create'),
    path('profiles/update/<int:pk>/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profiles/', UserProfileListView.as_view(), name='profile-list'),

    # Authentication
    path('login/', views.user_login, name='login'),

    # Downloads
    path('dwnlods/', views.cheatsheet, name='cheatsheet'),
    path('download/<int:Applications_Approval_id>/', download_cheatsheet, name='download_cheatsheet'),

    # Account Activation
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # Search
    path('search/', search_view, name='search'),
]
