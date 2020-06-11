from django.contrib import admin

from base_site.brokes_note.models import Broker
from base_site.brokes_note.models import BrokersNote
from base_site.brokes_note.models import BrokersNoteItem
from base_site.brokes_note.models import Company


class BrokerAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class BrokersNoteItemInline(admin.TabularInline):
    model = BrokersNoteItem


class BrokersNoteAdmin(admin.ModelAdmin):

    inlines = [
        BrokersNoteItemInline,
    ]


class BrokersNoteItemAdmin(admin.ModelAdmin):
    list_display = (
        "note",
        "company",
        "unit",
        "value",
    )


admin.site.register(Broker, BrokerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(BrokersNote, BrokersNoteAdmin)
admin.site.register(BrokersNoteItem, BrokersNoteItemAdmin)

# list_display = (
#     "db_included_date_time",
#     "category",
#     "name",
#     "description",
#     "debit",
#     "credit",
#     "payment_date_time",
#     "create_date_time",
# )
# readonly_fields = ("db_included_date_time",)
# list_filter = ("category", "name", "type_entry", "payment_date_time", "create_date_time")
