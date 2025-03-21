from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import TelegramUsers


@admin.register(TelegramUsers)
class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "chat_id", "language", "created_at", "updated_at")
    list_filter = ("language", "created_at", "updated_at")
    search_fields = ("chat_id", "username", "full_name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="telegram_users.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Full Name", "Username", "Chat ID", "Language", "Created At", "Updated At"])

        for user in queryset:
            writer.writerow(
                [user.id, user.full_name, user.username, user.chat_id, user.language, user.created_at, user.updated_at])

        return response

    export_as_csv.short_description = "Export selected as CSV"
