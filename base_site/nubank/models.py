from base_site.mainapp.models import Category
from base_site.mainapp.models import FamilyMember
from base_site.mainapp.models import TypeEntry
from django.contrib.postgres.fields import JSONField
from django.db import models


class NubankStatement(models.Model):

    created_at = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(max_digits=9, decimal_places=2)
    amount_without_iof = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2)
    description = models.CharField(blank=True, null=True, max_length=200)
    category = models.CharField(blank=True, null=True, max_length=80)
    source = models.CharField(blank=True, null=True, max_length=40)
    title = models.CharField(blank=True, null=True, max_length=200)
    account = models.CharField(blank=True, null=True, max_length=40)
    details = JSONField(blank=True, null=True)
    nubank_id = models.CharField(blank=True, null=True, max_length=40, db_index=True, verbose_name="id")
    href = models.CharField(blank=True, null=True, max_length=200)
    item_time = models.DateTimeField()
    is_processed = models.BooleanField(default=False)


class NubankSession(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=100)


class NubankCards(models.Model):

    command_1 = models.CharField(max_length=11)
    command_2 = models.CharField(max_length=11)

    cpf = models.CharField(max_length=11)
    last_login = models.DateTimeField(null=True, blank=True)


class NubankItemSetup(models.Model):
    description = models.CharField(max_length=200)
    description_slug = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria", blank=True, null=True)
    name = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, blank=True, verbose_name="Nome", null=True)
    type_entry = models.ForeignKey(TypeEntry, on_delete=models.CASCADE, verbose_name="Tipo", blank=True, null=True)

    is_credit = models.BooleanField(default=False)
