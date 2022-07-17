import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import ParetosUser
from .forms import *


def home(request):
    username = request.user.get_username()
    members_number = len(ParetosUser.objects.all())
    context = {"username": username, "members_number": members_number}
    return render(request, "home.html", context=context)


def login_user(request):
    if request.session.get('text'):
        text = request.session.pop('text')
        form = LoginForm()
        return render(request, 'login.html', context={"form": form, "text": text})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                text = "Hallo {0}. Du bist jetzt angemeldet".format(
                    user.get_username())
                return render(request, 'success.html', context={"text": text})
            else:
                return render(request, 'no_success.html', context={})
        else:
            # if form is not valid we need to show errors
            return render(request, 'login.html', context={"form": form})

    else:
        form = LoginForm()
        return render(request, 'login.html', context={"form": form})


def generate_token():
    # TODO: improve here
    r = [str(x) for x in random.sample(range(0, 9), 6)]
    return int("".join(r))


def register_user(request):
    if request.session.get('register_text'):
        text = request.session.pop('register_text')
        form = RegisterForm()
        return render(request, 'register.html', context={"form": form, "text": text})

    if request.method != 'POST':
        form = RegisterForm()
        return render(request, 'register.html', context={"form": form})
    else:
        form = RegisterForm(request.POST)
        if not(form.is_valid()):
            return render(request, 'register.html', context={"form": form})

        # TODO: isolate this part here...
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        token = generate_token()
        user = ParetosUser(
            username=username,
            email=email,
            password=password,
            email_confirmation_token=token,
        )
        # TODO: need to check how to do this properly
        user.set_password(password)
        user.save()
        user.send_activation_email(request)
        login(request, user)
        text = "Hallo {0}. Wir haben dir eine E-Mail gesendet.".format(
            username)
        return render(request, 'success.html', context={"text": text})


def email_activation(request, username, token):
    try:
        user = ParetosUser.objects.get(username=username)
        user.activate_mail(token)
        return render(request, "success.html", context={"text": "Danke. Wir haben deine E-mail aktiviert."})
    except:
        return render(request, "success.html", context={"text": "There was an error"})


def logout_user(request):
    logout(request)
    return logout_view(request)


def logout_view(request):
    return render(request, 'logout.html')


def get_ParetosUser_by_username_or_mail(username_or_mail):
    # TODO: make this better

    try:
        return ParetosUser.objects.get(username=username_or_mail)
    except:
        try:
            return ParetosUser.objects.get(email=username_or_mail)
        except:
            return None


def request_reset_password(request):
    if request.method == 'POST':
        form = RequestResetPasswordForm(request.POST)
        if form.is_valid():
            # TODO: validate form first before sending email
            username_or_mail = form.cleaned_data["username_or_mail"]
            user = get_ParetosUser_by_username_or_mail(username_or_mail)
            if user is not None:
                token = generate_token()
                user.set_password_reset_token(token)
                user.send_reset_mail(request)
                text = "Wir haben dir eine Mail gesendet..."
                return render(request, "success.html", context={"text": text})

            text = "Es gibt kein Account mit diesem Benutzername\n"
            text += "Erstelle einen neuen Account."
            request.session["register_text"] = text
            return redirect("register_user")
    else:
        form = RequestResetPasswordForm()
        return render(request, 'request_reset_password.html', context={"form": form})


def reset_password(request, username, token):
    try:
        user = ParetosUser.objects.get(username=username)
    except:
        return render(request, "no_success.html")

    if str(user.password_reset_token) != token:
        # wrong token
        return render(request, "no_success.html")

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            user.set_password(new_password)
            user.save()
            request.session["text"] = "Melde dich jetzt mit deinem neuen Passwort an."
            return redirect("login_user")
        else:
            return render(request, 'reset_password.html', context={"form": form})

    else:
        form = ResetPasswordForm()
        return render(request, 'reset_password.html', context={"form": form})


def test(request):
    username = request.user.get_username()
    context = {"username": username}
    return render(request, 'test.html', context=context)
