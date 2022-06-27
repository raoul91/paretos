from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from urllib.parse import urljoin
import random

global EMAIL_HOST_USER
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


class ParetosUser(User):

    email_confirmed = models.BooleanField(default=False)
    email_confirmation_token = models.IntegerField()

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

    def send_reset_mail(self, request):
        # TODO: this is still very insecure
        # Need to generate a token and put it into uri
        print("SENDING RESET EMAIL TO {0}".format(self.email))
        message = "Hallo {0}\n\n".format(self.username)
        reset_url = request.build_absolute_uri(
            "/reset/{user}/".format(user=self.username))
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
