from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def __create_user(self, site, email, password=None):
        if not email:
            raise ValueError(_('User must have an email address.'))
        try:
            site = Site.objects.get(id=site)
        except Site.DoesNotExist:
            raise ValueError(_('Site ID is invalid.'))
        user = self.model(
            site=site,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        return user

    def create_user(self, site, email, password=None):
        user = self.__create_user(site, email, password)
        user.save(using=self._db)
        return user

    def create_superuser(self, site, email, password):
        user = self.__create_user(site, email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    site = models.ForeignKey(
        Site,
        related_name='users',
        null=False,
        blank=False,
        db_index=True,
    )
    email = fields.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )
    first_name = fields.CharField(
        verbose_name=_('First Name'),
        max_length=32,
        null=True,
        blank=False,
    )
    last_name = fields.CharField(
        verbose_name=_('Last Name'),
        max_length=32,
        null=True,
        blank=False,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    create_date = fields.DateTimeField(
        verbose_name=_('Create Date'),
        null=False,
        blank=True,
        auto_now_add=True,
    )
    update_date = fields.DateTimeField(
        verbose_name=_('Update Date'),
        null=True,
        blank=True,
        auto_now=True,
    )

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['site']

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        get_latest_by = 'create_date'
        default_related_name = 'users'

    def get_short_name(self):
        return self.first_name if self.first_name is not None else self.email

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.email
