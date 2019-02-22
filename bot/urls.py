from django.conf.urls import (
    url,
)
from django.views.decorators.csrf import csrf_exempt

from .views import (
    checkout_view,
    home_view,
    sandbox_chatbot_plugin_view,
    WebhooksView,
    CustomAuthToken,
)

from .user_views import (
    get_user_profile,
    PostToken,
    # get_data,
)

profile = [
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', get_user_profile, name='profile'),
]


bot = [
    url(r'^get_data/', PostToken.as_view(), name='get_data'),
    url(r'^$', home_view, name='home'),
    url(r'^webview/', checkout_view, name='checkout'),
    url(r'^sandbox/', csrf_exempt(sandbox_chatbot_plugin_view), name='sandbox'),
    # API
    url(r'^webhook/', WebhooksView.as_view(), name='webhook'),
    url(r'^api-token-auth/', CustomAuthToken.as_view())
]

urlpatterns = bot + profile
