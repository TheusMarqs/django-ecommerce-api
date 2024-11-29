from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group, Permission
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.token

    @staticmethod
    def calculate_expiration():
        """
        Calcula a data de expiração com base na configuração do SIMPLE_JWT.
        """
        from datetime import datetime
        from rest_framework_simplejwt.settings import api_settings

        lifetime = api_settings.REFRESH_TOKEN_LIFETIME  # Duração configurada no SIMPLE_JWT
        return datetime.now() + lifetime

@receiver(post_save, sender=BlacklistedToken)
def clean_expired_tokens(sender, instance, **kwargs):
    BlacklistedToken.objects.filter(expires_at__lt=datetime.now()).delete()
    

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Define um related_name único
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_query_name="custom_user",  # Define um related_query_name único
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Define um related_name único
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
        related_query_name="custom_user",  # Define um related_query_name único
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]