from django import forms
from .models import ParetosUser
#from django.contrib.auth import authenticate, login, logout


# TODO: put this somewhere else
def is_already_existent(username):
    try:
        ParetosUser.objects.get(username=username)
        return True
    except:
        return False


class RegisterForm(forms.Form):

    button_label = "Registrieren"

    username = forms.CharField(required=True, label="Benutzername")
    email = forms.EmailField(required=True, label="E-Mail")
    email_confirmation = forms.EmailField(
        required=True,
        label="E-Mail bestätigen")
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label="Passwort")

    def clean(self):
        super(RegisterForm, self).clean()

        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        email_confirmation = self.cleaned_data["email_confirmation"]
        password = self.cleaned_data["password"]

        if email != email_confirmation:
            raise forms.ValidationError('Email Adressen stimmen nicht überein')
        if len(password) < 4:
            raise forms.ValidationError('Passwort ist zu kurz')

        if is_already_existent(username):
            raise forms.ValidationError(
                "Benutzer existiert schon. Melde dich an.")

        # TODO: implement better logic for password
        return self.cleaned_data


class LoginForm(forms.Form):

    button_label = "Anmelden"

    username = forms.CharField(required=True, label="Benutzername")
    password = forms.CharField(
        required=True, label="Passwort", widget=forms.PasswordInput())

    def clean(self):
        super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not(is_already_existent(username)):
            raise forms.ValidationError("Benutzername existiert nicht.")
        else:
            user = ParetosUser.objects.get(username=username)
            if not(user.check_password(password)):
                raise forms.ValidationError("Falsches Passwort.")

        return self.cleaned_data


class RequestResetPasswordForm(forms.Form):
    button_label = "Link senden"

    username_or_mail = forms.CharField(
        required=True, label="Benutzername oder E-Mail")

    # TODO: Check if user exists first


class ResetPasswordForm(forms.Form):
    button_label = "Passwort ändern"

    new_password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Neues Passwort")
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Neues Passwort bestätigen")

    def clean(self):
        super(ResetPasswordForm, self).clean()
        new_password = self.cleaned_data["new_password"]
        new_password_confirm = self.cleaned_data["new_password_confirm"]
        if new_password != new_password_confirm:
            raise forms.ValidationError("Passwörter stimmen nicht überein")

        # TODO: implement better logic for password
        return self.cleaned_data
