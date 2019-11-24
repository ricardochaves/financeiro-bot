from base_site.alelo.models import AleloItem
from base_site.alelo.models import AleloItemSetup
from django.contrib import admin


class AleloItemAdmin(admin.ModelAdmin):
    list_display = ("item_date", "is_processed", "description", "icon", "item_type", "value")
    list_filter = ("is_processed", "item_date")


class AleloItemSetupAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "name", "type_entry", "is_credit")


admin.site.register(AleloItem, AleloItemAdmin)
admin.site.register(AleloItemSetup, AleloItemSetupAdmin)
