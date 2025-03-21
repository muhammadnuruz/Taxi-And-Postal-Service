from django.db import models


class Drivers(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return self.name
