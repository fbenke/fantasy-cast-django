import random
from hashlib import sha1

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, username=None):
        if not email or not password:
            raise ValueError('Users must have an email address and password')

        user = self.model(email=self.normalize_email(email))
        user.set_username(username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def set_username(self, username=None):

        if username:
            self.username = username
            return

        while True:
            username = sha1(str(random.random()).encode(
                'utf-8')).hexdigest()[:5]
            try:
                CustomUser.objects.get(username__iexact=username)
            except CustomUser.DoesNotExist:
                self.username = username
                break

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class EmailOrUsernameModelBackend(object):

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = CustomUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return CustomUser.objects.get(pk=username)
        except CustomUser.DoesNotExist:
            return None
