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
    username = forms.CharField(widget=WIDGET, required=True)
    email = forms.EmailField(widget=WIDGET, required=True)
    email_confirmation = forms.EmailField(widget=WIDGET, required=True)
    password = forms.CharField(widget=PASSWORD_WIDGET, required=True)

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

        # TODO: make this better
        u = authenticate(username=name, password=password)
        if u is not None:
            print("USER IS NOT NONE")
            print(u.__class__)
        else:
            print("Authentication failed miserably")
        try:
            user = ParetosUser.objects.get(username=name)
            if not user.check_password(password):
                self._errors["password"] = "Falsches Passwort"

        except:
            user = None
            self._errors["name"] = "Benutzername existiert nicht"


class EmailActivationForm(forms.Form):
    widget = forms.TextInput(attrs={'class': 'form-control'})

    username = forms.CharField(
        widget=WIDGET, required=True, label="Benutzername")
    password = forms.CharField(
        widget=PASSWORD_WIDGET, required=True, label="Passwort")
    token = forms.CharField(
        widget=WIDGET, required=True, label="Aktivierungscode")

    def clean(self):
        super(EmailActivationForm, self).clean()
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        token = self.cleaned_data["token"]

        # TODO: use authenticate method at this point
        u = authenticate(username=username, password=password)
        if u is not None:
            print("AUTHENTICATED")
        else:
            print("NOT AUTH")

        try:
            user = ParetosUser.objects.get(username=username)
            if not(user.check_password(password)):
                self._errors["password"] = "Falsches Passwort"

            if str(token) != str(user.email_confirmation_token):
                self._errors["token"] = "Falscher Bestätigungscode."
        except:
            user = None
            self._errors["username"] = "Benutzername existiert nicht"


class RequestResetPasswordForm(forms.Form):
    username_or_mail = forms.CharField(
        widget=WIDGET, required=True, label="Benutzername oder E-Mail")

    # TODO: Check if user exists first


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=PASSWORD_WIDGET, required=True)
    new_password_confirm = forms.CharField(
        widget=PASSWORD_WIDGET, required=True)

    def clean(self):
        super(ResetPasswordForm, self).clean()
        new_password = self.cleaned_data["new_password"]
        new_password_confirm = self.cleaned_data["new_password_confirm"]
        if new_password != new_password_confirm:
            self._errors["new_password_confirm"] = "Passwörter stimmen nicht überein"
