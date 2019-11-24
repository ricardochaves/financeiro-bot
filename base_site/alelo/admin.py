from base_site.alelo.models import AleloItem
from django.contrib import admin


class AleloItemAdmin(admin.ModelAdmin):
    list_display = ("item_date", "description", "icon", "item_type", "value")


admin.site.register(AleloItem, AleloItemAdmin)
