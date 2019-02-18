
from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from bot.chatbot_plugin.app import integrations
from bot.chatbot_plugin.app.agents.builder import (
    build_agent_by_intent_diplayname,
)


from app.auth import TokenAuthSupportQueryString
from app.settings import DEBUG

from .utils import get_required_params
from .decorators import timing_and_reporting
from .api_exceptions import ServiceUnavailable


def home_view(request):
    """View function for home page of site."""
    return render(request, 'bot/home.html')


def checkout_view(request):
    """
    View function for webiew page to render embedded checkout.
    GET:
    - eid = <event_id>
    """
    context = {
        'eb_emb_chkout_src': integrations.eventbrite.get_widgets(debug=DEBUG),
        'prev_msg': 'Loading...'
    }
    return render(request, 'bot/webview.html', context=context)


def sandbox_chatbot_plugin_view(request):
    """View function for chatbot plugin sandbox."""
    context = {
        'actions': integrations.sandbox.CONTEXT_ACTIONS,
        'debug': DEBUG,
    }
    if request.method == 'POST':
        post = request.POST
        agent = build_agent_by_intent_diplayname('SandBox')
        agent.process_request(post)
    return render(request, 'bot/sandbox.html', context=context)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class WebhooksView(APIView):
    """
    View to trigger actions in the app.

    * token = Requires token authentication.
    * Only users authenticated are able to access this view.
    * format=json to parse data

    POST (async):
    - agent or intent
    - lang_code

    GET (sync):
    - agent
    - lang_code
    """
    authentication_classes = (TokenAuthSupportQueryString,)
    permission_classes = (permissions.IsAuthenticated,)

    @timing_and_reporting
    def get(self, request, format=None):
        """
        GET: Agent processor
        """
        params = request.query_params

        agent = build_agent_by_intent_diplayname(params.get('agent', None))
        agent.request_url = request.build_absolute_uri('/')
        agent.lang_code = params.get('lang_code', None)
        try:
            return_value = agent.process_request(params)
        except Exception:
            raise ServiceUnavailable()
        return Response(return_value)

    def post(self, request, format=None):
        """
        POST: Agent processor
        """
        params = get_required_params(post=request.data, url=request.build_absolute_uri('/'))

        if params.get('agent_name'):
            agent = build_agent_by_intent_diplayname(params.get('agent_name'))
            agent.request_url = params.get('url')
            # param: languageCode
            agent.lang_code = params.get('lang_code')
            try:
                return_value = agent.process_request(request.data)
                print(return_value)
            except Exception:
                raise ServiceUnavailable()
        else:
            raise ServiceUnavailable()

        return Response(params)


class CustomAuthToken(ObtainAuthToken):
    """
    View to generate auth token.
    Since version 3.6.4 it's possible to generate a user token using the following command:
    ./manage.py drf_create_token <username>

    POST: http://127.0.0.1:8000/api-token-auth/
    body:
    - username:
    - password:
    return:
    {
        "token": "XX",
        "user_id": X,
        "email": "X"
    }
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
