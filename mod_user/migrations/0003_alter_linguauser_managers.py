# Generated by Django 4.2 on 2023-05-05 06:33

from django.db import migrations
import mod_user.models


class Migration(migrations.Migration):

    dependencies = [
        ('mod_user', '0002_alter_linguauser_birthdate'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='linguauser',
            managers=[
                ('objects', mod_user.models.LinguaUserManager()),
            ],
        ),
    ]
