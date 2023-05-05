from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from datetime import date


class LinguaUserManager(UserManager):
    use_in_migrations = True
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Please provide email")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("birthdate", date.today())
        user = self.create_user(username, email, password, **extra_fields)

        return user


class LinguaUser(AbstractUser):
    class GenderChoice(models.TextChoices):
        MALE = 'MALE', _('MALE')
        FEMALE = 'FEMALE', _('FEMALE')

    birthdate = models.DateField(null=True)
    gender = models.CharField(
        max_length=20,
        choices=GenderChoice.choices,
        default=GenderChoice.MALE
    )

    objects = LinguaUserManager()

    class Meta:
        db_table = 'LINGUA_USER'
        db_table_comment = 'user used for lingualink app'

