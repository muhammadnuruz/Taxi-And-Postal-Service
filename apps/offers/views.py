from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.offers.models import Offers
from apps.offers.serializers import OffersCreateSerializer


class CreateOfferView(CreateAPIView):
    queryset = Offers.objects.all()
    serializer_class = OffersCreateSerializer
    permission_classes = [AllowAny]
