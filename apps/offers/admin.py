from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.http import HttpResponse
import csv
from .models import Offers


@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "colored_offer_type", "colored_passengers", "phone_number", "created_at")
    list_filter = ("offer_type", "number_of_passengers", "delivery_address", "created_at")
    search_fields = ("full_name", "phone_number", "delivery_address")
    ordering = ("-created_at",)
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Info", {
            "fields": ("chat_id", "full_name", "phone_number")
        }),
        ("Offer Details", {
            "fields": ("offer_type", "number_of_passengers", "delivery_address")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    actions = ["export_to_csv", "mark_as_passenger", "mark_as_mail"]

    def colored_offer_type(self, obj):
        colors = {"mail": "blue", "passenger": "green"}
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>',
                           colors.get(obj.offer_type, "black"), obj.get_offer_type_display())

    colored_offer_type.short_description = "Offer Type"

    def colored_passengers(self, obj):
        if obj.number_of_passengers:
            return format_html(
                '<span style="background-color: lightgray; padding: 3px 8px; border-radius: 5px;">{}</span>',
                obj.number_of_passengers)
        return "-"

    colored_passengers.short_description = "Passengers"

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="offers.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Full Name", "Offer Type", "Passengers", "Phone", "Address", "Created At"])

        for offer in queryset:
            writer.writerow([
                offer.id, offer.full_name, offer.offer_type, offer.number_of_passengers or "-",
                offer.phone_number, offer.delivery_address, offer.created_at
            ])
        return response

    export_to_csv.short_description = "Export to CSV"

    def changelist_view(self, request, extra_context=None):
        offer_stats = Offers.objects.values("offer_type").annotate(count=Count("offer_type"))
        extra_context = extra_context or {}
        extra_context["offer_stats"] = offer_stats
        return super().changelist_view(request, extra_context=extra_context)
