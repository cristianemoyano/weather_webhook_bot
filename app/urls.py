from django.contrib import (
    admin,
)
from django.conf.urls import (
    include,
    url,
)

urlpatterns = [
    url(r'', include('bot.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
]
