from rest_framework import serializers
from .models import Drivers


class DriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = ["id", "name", "phone_number", "chat_id", "created_at", "updated_at"]
