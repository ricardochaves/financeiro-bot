from base_site.nubank.models import NubankCards
from base_site.nubank.models import NubankStatement
from django.contrib import admin


class NubankCardsAdmin(admin.ModelAdmin):
    list_display = ("command_1", "command_2", "cpf", "last_login")


admin.site.register(NubankCards, NubankCardsAdmin)


class NubankStatementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "is_processed", "amount", "category", "item_time", "title")
    list_filter = ("is_processed", "created_at", "item_time")


admin.site.register(NubankStatement, NubankStatementAdmin)
