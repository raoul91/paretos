# Generated by Django 4.0.5 on 2022-06-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paretosuser',
            name='email_confirmation_token',
            field=models.IntegerField(),
        ),
    ]
