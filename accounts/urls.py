from django.urls import path
from django.conf.urls import (
    url,
)

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.UserProfileView, name='profile'),
    path('pages/', views.DefaultSocialPageView, name='social-pages'),
]
