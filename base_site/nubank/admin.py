from base_site.nubank.models import NubankCards
from base_site.nubank.models import NubankItemSetup
from base_site.nubank.models import NubankStatement
from django.contrib import admin


class NubankCardsAdmin(admin.ModelAdmin):
    list_display = ("command_1", "command_2", "cpf", "last_login")


class NubankStatementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "is_processed", "amount", "description", "item_time", "title")
    list_filter = ("is_processed", "created_at", "item_time")
    ordering = ["-created_at"]


class NubankItemSetupAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "name", "type_entry", "is_credit")
    prepopulated_fields = {"description_slug": ("description",)}


admin.site.register(NubankStatement, NubankStatementAdmin)
admin.site.register(NubankItemSetup, NubankItemSetupAdmin)
admin.site.register(NubankCards, NubankCardsAdmin)
