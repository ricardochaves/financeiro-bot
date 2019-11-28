from base_site.nubank.models import NubankCards
from base_site.nubank.models import NubankStatement
from django.contrib import admin


class NubankCardsAdmin(admin.ModelAdmin):
    pass
    # list_display = ("item_date", "is_processed", "description", "icon", "item_type", "value")
    # list_filter = ("is_processed", "item_date")


admin.site.register(NubankCards, NubankCardsAdmin)


class NubankStatementAdmin(admin.ModelAdmin):
    pass
    # list_display = ("item_date", "is_processed", "description", "icon", "item_type", "value")
    # list_filter = ("is_processed", "item_date")


admin.site.register(NubankStatement, NubankStatementAdmin)
