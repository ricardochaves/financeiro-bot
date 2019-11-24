from base_site.alelo.models import AleloItem
from base_site.alelo.models import AleloItemSetup
from django.contrib import admin


class AleloItemAdmin(admin.ModelAdmin):
    list_display = ("item_date", "description", "icon", "item_type", "value")


admin.site.register(AleloItem, AleloItemAdmin)


class AleloItemSetupAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "name", "type_entry", "is_credit")


admin.site.register(AleloItem, AleloItemAdmin)
admin.site.register(AleloItemSetup, AleloItemSetupAdmin)
