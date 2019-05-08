from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from mainapp.models import Category
from mainapp.models import FamilyMember
from mainapp.models import FullCommand
from mainapp.models import Records
from mainapp.models import TypeEntry

admin.site.register(FullCommand)


class CategoryAdmin(ImportExportModelAdmin):
    pass


class FamilyMemberAdmin(ImportExportModelAdmin):
    pass


class TypeEntryAdmin(ImportExportModelAdmin):
    pass


class RecordsAdmin(ImportExportModelAdmin):
    list_display = (
        "db_included_date_time",
        "category",
        "name",
        "description",
        "debit",
        "credit",
        "payment_date_time",
        "create_date_time",
    )
    readonly_fields = ("db_included_date_time",)
    list_filter = ("category", "name", "type_entry", "payment_date_time", "create_date_time")


admin.site.register(Records, RecordsAdmin)
admin.site.register(TypeEntry, TypeEntryAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Category, CategoryAdmin)
