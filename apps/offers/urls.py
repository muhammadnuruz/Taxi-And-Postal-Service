from django.urls import path

from apps.offers.views import CreateOfferView

urlpatterns = [
    path("create/", CreateOfferView.as_view(), name="create-offer")
]
