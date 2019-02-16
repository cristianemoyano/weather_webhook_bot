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

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^webview/', checkout_view, name='checkout'),
    url(r'^sandbox/', csrf_exempt(sandbox_chatbot_plugin_view), name='sandbox'),
    # API
    url(r'^webkooks/', WebhooksView.as_view(), name='webkooks'),
    url(r'^api-token-auth/', CustomAuthToken.as_view())
]
