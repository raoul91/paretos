from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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

    def send_confirmation_email(self, request):
        print("SENDING CONFIRMATION EMAIL TO {0}".format(self.email))
        message = "hello"
        confirmation_url = request.build_absolute_uri("confimation")
        message += "Confirm your email via this link: {0}\n".format(
            confirmation_url)
        message += "Here is your confirmation token: {0}".format(
            self.email_confirmation_token)
        self.email_user(
            subject="TEST Confirm Mail",
            message=message,
            from_email=EMAIL_HOST_USER,
        )

    def send_reset_mail(self, request):
        # TODO: this is still very insecure
        # Need to generate a token and put it into uri
        print("SENDING RESET EMAIL TO {0}".format(self.email))
        message = "hello"
        reset_url = request.build_absolute_uri(
            "/reset/{user}/".format(user=self.username))
        message += "Reset your email via this link: {0}\n".format(
            reset_url)
        self.email_user(
            subject="TEST Reset Mail",
            message=message,
            from_email=EMAIL_HOST_USER,
        )

    def set_email_confimation_flag(self):
        self.email_confirmed = True
        self.save()
