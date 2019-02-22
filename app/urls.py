from django.contrib import (
    admin,
)
from django.conf.urls import (
    include,
    url,
)
from django.urls import path

"""
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
"""
login = [
    path('accounts/', include('django.contrib.auth.urls')),
]

apps = [
    # Home and bot.urls
    url(r'', include('bot.urls')),
    # django rest framework
    url(r'^api-auth/', include('rest_framework.urls')),
    # adming
    url(r'^admin/', admin.site.urls),
]

urlpatterns = login + apps
