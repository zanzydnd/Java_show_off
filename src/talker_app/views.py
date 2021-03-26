from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from talker_app.forms import RegistrationForm, AuthForm, TalkForm, TalkAnswerForm
from talker_app.models import Talk, TalkAnswer


class AuthView(View):
    def get(self,request):
        return render(request,"login/login.html")

    def post(self,request):
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            lg = authenticate(username=username, password=password)

            if lg is None:
                errors = {
                    "error": "wrong login or pass"
                }
                return render(request, 'login/login.html', errors)
            else:
                login(request, lg)
                return redirect('home')
        else:
            return redirect('login')

def registration(request):
    if request.method == "GET":
        return render(request,"login/registration.html")
    elif request.method == "POST":
        new_user = RegistrationForm(request.POST)

        if new_user:
            if new_user.is_valid():
                username = new_user.cleaned_data['username']
                email = new_user.cleaned_data['email']
                password = new_user.cleaned_data['password']
                all_emails = User.objects.filter(email=email)
                if all_emails:
                    errors ={
                        "error_email" : "Почта занята"
                    }
                    return render(request,'login/registration.html',errors)
                else:
                    password = make_password(password)
                    User.objects.create(username=username, email=email, password=password)
                    return redirect('login')

def home_page(request):
    user = request.user
    if request.user.is_authenticated is False:
        user = None
    talks = Talk.objects.order_by('-date')[:10]
    context = {
        'user': user,
        'talks_list': talks
    }
    return render(request, 'talker/main_page.html', context)

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def create_talk_view(request):
    if request.user.is_authenticated:
        tlk_form = TalkForm(request.POST or None)
        if tlk_form.is_valid():
            text = tlk_form.cleaned_data['text']
            Talk.objects.create(text=text, author=request.user)
        return redirect('home')
    else:
        return redirect('login')


def profile_view(request, username):
    user = request.user
    if request.user.is_authenticated is False:
        user = None
    if request.method == "GET":
        user_whos_profile_being_watched = get_object_or_404(User, username=username)
        talks_list = Talk.objects.filter(author=user_whos_profile_being_watched).order_by('-date')
        context = {
            'talks_list': talks_list,
            'user_profile': user_whos_profile_being_watched,
            'user': user
        }
        return render(request, 'talker/profile.html', context)
    else:
        return redirect('home')


def talk_view(request, talk_id):
    user = request.user
    if request.user.is_authenticated is False:
        user = None
    if request.method == "GET":
        talk = Talk.objects.get(pk=talk_id)
        answers = TalkAnswer.objects.filter(head_talk_id=talk_id).order_by('-date')

        context = {
            'user': user,
            'talk': talk,
            'answers': answers
        }
        return render(request, 'talker/talk.html', context)

@login_required
def answer_view(request, talk_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            head_talk = Talk.objects.get(pk=talk_id)
            answ_form = TalkAnswerForm(request.POST or None)
            print(answ_form.errors)
            if answ_form.is_valid():
                text = answ_form.cleaned_data['text']
                TalkAnswer.objects.create(text=text, author=request.user, head_talk=head_talk)
                return redirect('talk_page', talk_id)
            else:
                return redirect('home')