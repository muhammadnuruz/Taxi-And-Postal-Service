from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Drivers


@admin.register(Drivers)
class DriversAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "chat_id", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "chat_id")
    search_fields = ("name", "phone_number", "chat_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="drivers.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Name", "Phone Number", "Chat ID", "Created At", "Updated At"])

        for driver in queryset:
            writer.writerow(
                [driver.id, driver.name, driver.phone_number, driver.chat_id, driver.created_at, driver.updated_at])

        return response

    export_as_csv.short_description = "Export selected as CSV"
