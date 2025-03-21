from django.db import models


class TelegramUsers(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Russian'),
        ('uz', 'Uzbek'),
        ('kr', 'Krill')
    ]
    chat_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='uz')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"

    def __str__(self):
        return f"{self.full_name}"
