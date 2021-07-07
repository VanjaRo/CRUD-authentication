import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if username is None:
            raise TypeError('Users must have a username.')
        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(username=username)
        print(password)
        user.set_password(password)
        print(user.password)
        user.save()
        print(user.password)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=150, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.JWT_SECRET_KEY)

        return token
