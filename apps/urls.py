from django.urls import path, include


urlpatterns = [
    path('telegram-users/', include("apps.telegram_users.urls")),
    path('offers/', include("apps.offers.urls")),
    path('drivers/', include("apps.drivers.urls")),
]
