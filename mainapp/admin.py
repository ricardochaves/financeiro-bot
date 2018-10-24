from django.contrib import admin

from mainapp.models import Category
from mainapp.models import FamilyMember
from mainapp.models import FullCommand
from mainapp.models import Records
from mainapp.models import TypeEntry

admin.site.register(TypeEntry)
admin.site.register(FamilyMember)
admin.site.register(Category)
admin.site.register(FullCommand)


class RecordsAdmin(admin.ModelAdmin):
    list_display = ("db_included_date_time", "category", "name", "description", "payment_date_time", "create_date_time")
    readonly_fields = ("db_included_date_time",)
    list_filter = ("category", "name", "type_entry", "payment_date_time", "create_date_time")


admin.site.register(Records, RecordsAdmin)
