from doctest import ELLIPSIS_MARKER
import email
import os
from email import message
import re
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import ParetosUser

from .forms import LoginForm, RegisterForm, ConfirmationForm, RequestResetPasswordForm, ResetPasswordForm


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
            username = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'success.html', context={"username": user.get_username()})
            else:
                return render(request, 'no_success.html', context={})
        else:
            # if form is not valid we need to show errors
            return render(request, 'login.html', context={"form": form})

    else:
        form = LoginForm()
        return render(request, 'login.html', context={"form": form})


def register_user(request):
    if request.session.get('register_text'):
        text = request.session.pop('register_text')
        form = RegisterForm()
        return render(request, 'register.html', context={"form": form, "text": text})

    if request.method != 'POST':
        form = RegisterForm()
        return render(request, 'register.html', context={"form": form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if not(form.is_valid()):
            return render(request, 'register.html', context={"form": form})

        # TODO: isolate this part here...
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        user = ParetosUser(
            username=username,
            email=email,
            password=form.cleaned_data["password"],
            email_confirmation_token=1234,
        )
        user.save()
        user.send_confirmation_email(request)
        login(request, user)
        context = {"username": username, "email": email}
        return render(request, 'success.html', context=context)


def confirmation(request):
    # TODO: need to do generate token or something like that
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if not(form.is_valid()):
            print("FORM IS NOT VALID")
            context = {"form": form}
            return render(request, "confirmation.html", context=context)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            token = form.cleaned_data["token"]

            try:
                user = ParetosUser.objects.get(username=username)
                user.set_email_confimation_flag()
                login(request, user)
                print("GEIL")
                return render(request, "success.html", context={})
            except:
                user = None
                return render(request, "no_success.html")

    else:
        form = ConfirmationForm()
        return render(request, 'confirmation.html', context={"form": form})


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
        pass

    try:
        return ParetosUser.objects.get(email=username_or_mail)
    except:
        pass

    return None


def request_reset_password(request):
    if request.method == 'POST':
        form = RequestResetPasswordForm(request.POST)
        if form.is_valid():
            # TODO: validate form first before sending email
            username_or_mail = form.cleaned_data["username_or_mail"]
            user = get_ParetosUser_by_username_or_mail(username_or_mail)
            if user is not None:
                user.send_reset_mail(request)
                return render(request, "success.html", context={"text": "Wir haben dir eine Mail gesendet..."})

            text = "No account was found with this username\n"
            text += "Please register a new account."
            request.session["register_text"] = text
            return redirect("register_user")
    else:
        form = RequestResetPasswordForm()
        return render(request, 'request_reset_password.html', context={"form": form})


def reset_password(request, username):
    # get user first, then reset password, then save
    try:
        user = ParetosUser.objects.get(username=username)
    except:
        return render(request, "no_success.html")

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            user.set_password(new_password)
            user.save()
            request.session["text"] = "You can login with your new password now"
            return redirect("login_user")

    else:
        form = ResetPasswordForm()
        return render(request, 'reset_password.html', context={"form": form})


def test(request):
    username = request.user.get_username()
    context = {"username": username}
    return render(request, 'test.html', context=context)
