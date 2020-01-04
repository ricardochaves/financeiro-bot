from django.contrib import admin

from base_site.alelo.models import AleloCard
from base_site.alelo.models import AleloItem
from base_site.alelo.models import AleloItemSetup


class AleloItemAdmin(admin.ModelAdmin):
    list_display = ("item_date", "is_processed", "description", "icon", "item_type", "value")
    list_filter = ("is_processed", "item_date")


class AleloItemSetupAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "name", "type_entry", "is_credit")


class AleloCardAdmin(admin.ModelAdmin):
    list_display = ("name", "last_numbers")


admin.site.register(AleloCard, AleloCardAdmin)
admin.site.register(AleloItem, AleloItemAdmin)
admin.site.register(AleloItemSetup, AleloItemSetupAdmin)
