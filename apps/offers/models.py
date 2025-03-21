from django.db import models


class Offers(models.Model):
    OFFER_TYPE_CHOICE = [
        ('mail', 'Mail'),
        ('passenger', 'Passenger'),
    ]
    ADDRESS_CHOICE = [
        ('tashkent-samarkand', 'Tashkent-Samarkand'),
        ('samarkand-tashkent', 'Samarkand-Tashkent'),
    ]
    PASSENGERS_CHOICE = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ]
    chat_id = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=50, choices=ADDRESS_CHOICE)
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPE_CHOICE)
    number_of_passengers = models.CharField(max_length=1, choices=PASSENGERS_CHOICE, null=True)
    phone_number = models.CharField(max_length=13)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        return self.full_name
