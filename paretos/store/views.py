from multiprocessing import context
import os
from email import message
import re
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import ParetosUser

from .forms import LoginForm, RegisterForm, ConfirmationForm, RequestResetPasswordForm, ResetPasswordForm


def home(request):
    username = request.user.get_username()
    print("USERNAME")
    print(username)
    return render(request, "home.html", context={"username": username})


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
                name = user.get_username()
                print("NAME: {name}".format(name=name))
                return render(request, 'success.html', context={"username": name})
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
        # TODO: improve here, pop key, value pair
        text = request.session['register_text']
        request.session['register_text'] = None
        form = RegisterForm()
        return render(request, 'register.html', context={"form": form, "text": text})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            # check if user exists
            # TODO: beautify
            try:
                user = ParetosUser.objects.get(username=username)
            except:
                user = None
            if user is None:
                print("USER DOES NOT EXIST YET")
                # mail authentication
                user = ParetosUser(
                    username=username,
                    email=email,
                    password=password,
                    email_confirmation_token=1234,
                )
                user.save()
                user.send_confirmation_email(request)
                return render(request, 'success.html', context={"username": username})

            if user is not None:
                request.session['text'] = "You are already registered. Login instead"
                return redirect("login_user")

    else:
        form = RegisterForm()
        return render(request, 'register.html', context={"form": form})


def confirmation(request):
    # TODO: need to do generate token or something like that
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            confirmation_token = form.cleaned_data["confirmation_token"]
            try:
                user = ParetosUser.objects.get(username=username)
            except:
                user = None
            # TODO: check authentication
            # TODO: change here...
            if user is not None:
                # set email confimation flag to true
                if user.email_confirmation_token == confirmation_token:
                    user.set_email_confimation_flag()
                    login(request, user)
                    context = {
                        "username": user.get_username(),
                        "text": "Your email has been verified."
                    }
                    return render(request, 'success.html', context=context)
                else:
                    print("WRONG EMAIL TOKEN")
                    return render(request, 'no_success.html', context={})
            else:
                return render(request, 'no_success.html', context={})

    else:
        form = ConfirmationForm()
        return render(request, 'confirmation.html', context={"form": form})


def logout_user(request):
    logout(request)
    return logout_view(request)


def logout_view(request):
    return render(request, 'logout.html')


def request_reset_password(request):
    if request.method == 'POST':
        form = RequestResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user = ParetosUser.objects.get(username=username)
                user.send_reset_mail(request)
                return render(request, "success.html", context={"text": "We just sent you an email to reset your password"})
            except:
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
