from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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


@login_required
def DefaultSocialPageView(request):
    if request.method == 'POST':
        social_id = request.POST.get('social_page')
        social_page_selected = SocialPages.objects.get(id=int(social_id))
        all_social_pages = SocialPages.objects.all()
        for page in all_social_pages:
            page.default = False
            page.save()
        social_page_selected.default = True
        social_page_selected.save()
        return redirect('accounts/profile/{}'.format(request.user.username))
    else:
        social_pages = SocialPages.objects.all().filter(user=request.user)
    return render(request, 'accounts/default_page.html', {'social_pages': social_pages})


@login_required
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
    absolute_url = request.build_absolute_uri('/')
    url_chatfuel = '{url}webhook/?agent=get_webview&event_id={evt}&user_id={user_id}&token={token}'.format(
        url=absolute_url,
        user_id='{{messenger user id}}',
        evt=45433408548,
        token=token
    )
    context = {
        "user": user,
        "social": social,
        "pages": pages,
        "token": token,
        "url_chatfuel": url_chatfuel,
    }
    return render(
        request,
        template_url,
        context
    )
