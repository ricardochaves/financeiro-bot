from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import TypeEntry
from django.db import models


class AleloItem(models.Model):

    item_date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2)
    item_type = models.CharField(max_length=20)
    icon = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    is_processed = models.BooleanField(default=False)


class AleloItemSetup(models.Model):
    description = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria", blank=True, null=True)
    name = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, blank=True, verbose_name="Nome", null=True)
    type_entry = models.ForeignKey(TypeEntry, on_delete=models.CASCADE, verbose_name="Tipo", blank=True, null=True)

    is_credit = models.BooleanField(default=False)
