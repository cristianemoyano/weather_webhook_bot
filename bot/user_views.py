from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SocialAccount


def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'bot/user_profile.html', {"user": user})


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
        token = params.get('token', None)
        username = params.get('username', None)
        social = None
        msg = 'Token exist'
        if token and username:
            user = User.objects.get(username=username)
            social = SocialAccount.objects.filter(user=user)
            if not social:
                SocialAccount.objects.create(
                    user=user,
                    token=token,
                    social='facebook'
                )
                msg = 'Token saved'
        return Response(msg)

    def post(self, request, format=None):
        """
        POST: Agent processor
        """
        params = request.data
        return Response(params)
