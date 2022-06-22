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
    name = forms.CharField(widget=WIDGET, required=True)
    email = forms.EmailField(widget=WIDGET, required=True)
    email_confirmation = forms.EmailField(widget=WIDGET, required=True)
    password = forms.CharField(widget=PASSWORD_WIDGET, required=True)

    def clean(self):
        super(RegisterForm, self).clean()

        email = self.cleaned_data["email"]
        email_confirmation = self.cleaned_data["email_confirmation"]
        password = self.cleaned_data["password"]

        if email != email_confirmation:
            self._errors['email_confirmation'] = self.error_class([
                'Email addressen stimmen nicht überein'])
        if len(password) < 4:
            self._errors["password"] = self.error_class([
                'Passwort ist zu kurz'])

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


class ConfirmationForm(forms.Form):
    widget = forms.TextInput(attrs={'class': 'form-control'})

    name = forms.CharField(widget=WIDGET, required=True, label="Benutzername")
    password = forms.CharField(
        widget=PASSWORD_WIDGET, required=True, label="Passwort")
    confirmation_token = forms.IntegerField(
        widget=PASSWORD_WIDGET, required=True, label="Bestätigungscode")

    def clean(self):
        super(ConfirmationForm, self).clean()
        # TODO: check if correct confirmation token


class RequestResetPasswordForm(forms.Form):
    username = forms.CharField(widget=WIDGET, required=True)


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=PASSWORD_WIDGET, required=True)
    new_password_confirm = forms.CharField(
        widget=PASSWORD_WIDGET, required=True)

    # TODO: verify if passwords match
