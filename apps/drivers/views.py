from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Drivers
from .serializers import DriversSerializer


class DriversListView(ListAPIView):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializer
    permission_classes = [AllowAny]
