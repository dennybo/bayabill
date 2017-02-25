from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def __create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        return user

    def create_user(self, email, password=None):
        user = self.__create_user(email, password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.__create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=32,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=32,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    create_date = models.DateTimeField(
        verbose_name=_('Create Date'),
        null=False,
        blank=False,
        auto_now_add=True,
    )

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.email
