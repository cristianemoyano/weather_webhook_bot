import json

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    SocialAccount,
    SocialPages,
)
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
            user = User.objects.get(username=username)
            pages = SocialPages.objects.filter(user=user)
            if not pages:
                page_data_json = get_page_data(access_token)
                page_data = json.loads(page_data_json)
                page_list = page_data.get('data')
                for page in page_list:
                    page_access_token = page.get('access_token')
                    page_category = page.get('category')
                    page_name = page.get('name')
                    page_id = page.get('id')
                    page_tasks = page.get('tasks')
                    SocialPages.objects.create(
                        user=user,
                        access_token=page_access_token,
                        category=page_category,
                        page_name=page_name,
                        page_id=page_id,
                        page_tasks=page_tasks
                    )
                social = SocialAccount.objects.filter(user=user)
                if not social:
                    SocialAccount.objects.create(
                        user=user,
                        token=access_token,
                        social='facebook'
                    )
                    msg = 'Token saved.'
                else:
                    msg = 'Token already exist.'
            else:
                msg = 'Pages saved.'
        return Response(msg)

    def post(self, request, format=None):
        """
        POST: Agent processor
        """
        params = request.data
        return Response(params)
