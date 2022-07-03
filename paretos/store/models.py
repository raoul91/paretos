from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

global EMAIL_HOST_USER
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


class ParetosUser(User):

    email_confirmed = models.BooleanField(default=False)
    email_confirmation_token = models.IntegerField()
    password_reset_token = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('username',)
        verbose_name = 'ParetosUser'

    def __str__(self):
        return self.username

    def get_activation_url(self, request):
        uri = "activate_email/{username}/{token}/".format(
            username=self.username,
            token=str(self.email_confirmation_token)
        )
        return request.build_absolute_uri(uri)

    def send_activation_email(self, request):
        message = "Hallo {0}\n\n".format(self.username)
        activation_url = self.get_activation_url(request)
        message += "Aktiviere deine E-Mail hier: {0}\n".format(
            activation_url)
        self.email_user(
            subject="Paretos.ch: Bestätige deine E-Mail Adresse",
            message=message,
            from_email=EMAIL_HOST_USER,
        )

    def get_reset_url(self, request):
        uri = "reset/{username}/{token}/".format(
            username=self.username,
            token=str(self.password_reset_token)
        )
        return request.build_absolute_uri(uri)

    def set_password_reset_token(self, token):
        self.password_reset_token = token
        self.save()

    def send_reset_mail(self, request):
        message = "Hallo {0}\n\n".format(self.username)
        reset_url = self.get_reset_url(request)
        message += "Ändere dein Passwort hier: {0}\n".format(
            reset_url)
        self.email_user(
            subject="Paretos.ch: Passwort Änderung",
            message=message,
            from_email=EMAIL_HOST_USER,
        )

    def activate_mail(self, token):
        if not(self.email_confirmed) and token == str(self.email_confirmation_token):
            self.email_confirmed = True
            self.save()
