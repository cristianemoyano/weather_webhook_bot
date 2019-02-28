from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import (
    redirect,
    render,
)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from bot.models import (
    SocialAccount,
    SocialPages,
)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts/profile/{}'.format(request.user.username))
        return super().get(request, *args, **kwargs)


def UserProfileView(request, username):
    template_url = 'accounts/user_profile.html'
    user = User.objects.get(username=username)
    social = SocialAccount.objects.filter(
        user=user
    )
    pages = SocialPages.objects.filter(
        user=user
    )
    token = Token.objects.get(
        user=user
    )
    context = {
        "user": user,
        "social": social,
        "pages": pages,
        "token": token,
    }
    return render(
        request,
        template_url,
        context
    )
