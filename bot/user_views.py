from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SocialAccount
from .utils import get_page_data


def get_user_profile(request, username):
    user = User.objects.get(username=username)
    social = SocialAccount.objects.filter(
        user=user
    )
    return render(request, 'bot/user_profile.html', {"user": user, "social": social})


class PostToken(APIView):
    """
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        """
        POST: Agent processor
        """
        params = request.GET
        access_token = params.get('token', None)
        username = params.get('username', None)
        social = None
        msg = 'Missing required params: token & username'
        if access_token and username:
            page_data = get_page_data(access_token)
            user = User.objects.get(username=username)
            social = SocialAccount.objects.filter(user=user)
            if not social:
                SocialAccount.objects.create(
                    user=user,
                    token=page_data,
                    social='facebook'
                )
                msg = 'Token saved.'
            else:
                msg = 'Token already exist.'
        return Response(msg)

    def post(self, request, format=None):
        """
        POST: Agent processor
        """
        params = request.data
        return Response(params)
