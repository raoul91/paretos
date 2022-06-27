from re import A
from django import forms
from .models import ParetosUser
from django.contrib.auth import authenticate, login, logout

# TODO: try to put this in html
WIDGET = forms.TextInput(
    attrs={'class': 'form-control'}
)

PASSWORD_WIDGET = forms.PasswordInput(
    attrs={'class': 'form-control', 'type': 'password',
           'name': 'password', 'placeholder': 'Passwort'}
)


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=WIDGET, required=True, label="Benutzername")
    email = forms.EmailField(widget=WIDGET, required=True, label="E-Mail")
    email_confirmation = forms.EmailField(
        widget=WIDGET, required=True, label="E-Mail bestätigen")
    password = forms.CharField(
        widget=PASSWORD_WIDGET, required=True, label="Passwort")

    def clean(self):
        super(RegisterForm, self).clean()

        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        email_confirmation = self.cleaned_data["email_confirmation"]
        password = self.cleaned_data["password"]

        if email != email_confirmation:
            self._errors['email_confirmation'] = 'Email Adressen stimmen nicht überein'
        if len(password) < 4:
            self._errors["password"] = 'Passwort ist zu kurz'
        try:
            ParetosUser.objects.get(username=username)
            self._errors['username'] = "Benutzer existiert schon. Melde dich an."
        except:
            pass

        # TODO: implement better logic for password


class LoginForm(forms.Form):
    name = forms.CharField(widget=WIDGET, required=True, label="Benutzername")
    password = forms.CharField(
        widget=PASSWORD_WIDGET, required=True, label="Passwort")

    def clean(self):
        super(LoginForm, self).clean()
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']

        user = authenticate(username=name, password=password)
        if user is not None:
            if not user.check_password(password):
                self._errors["password"] = "Falsches Passwort"
        else:
            self._errors["password"] = "Benutzername oder Passwort falsch."


class RequestResetPasswordForm(forms.Form):
    username_or_mail = forms.CharField(
        widget=WIDGET, required=True, label="Benutzername oder E-Mail")

    # TODO: Check if user exists first


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=PASSWORD_WIDGET, required=True, label="Neues Passwort")
    new_password_confirm = forms.CharField(
        widget=PASSWORD_WIDGET, required=True, label="Neues Passwort bestätigen")

    def clean(self):
        super(ResetPasswordForm, self).clean()
        new_password = self.cleaned_data["new_password"]
        new_password_confirm = self.cleaned_data["new_password_confirm"]
        if new_password != new_password_confirm:
            self._errors["new_password_confirm"] = "Passwörter stimmen nicht überein"
