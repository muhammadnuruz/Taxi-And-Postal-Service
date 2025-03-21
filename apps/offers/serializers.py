from rest_framework import serializers
from apps.offers.models import Offers


class OffersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ('chat_id', 'full_name', 'offer_type', 'delivery_address', 'number_of_passengers', 'phone_number')
