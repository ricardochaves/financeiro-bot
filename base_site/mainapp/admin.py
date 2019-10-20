from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import FullCommand
from base_site.mainapp.models import Records
from base_site.mainapp.models import TypeEntry
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

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
