from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

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