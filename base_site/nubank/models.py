from django.contrib.postgres.fields import JSONField
from django.db import models


class NubankItem(models.Model):

    created_at = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(max_digits=9, decimal_places=2)
    index = models.IntegerField()
    title = models.CharField(max_length=200)
    post_date = models.DateField()
    nubank_id = models.CharField(max_length=40)
    href = models.CharField(max_length=200)
    category = models.CharField(max_length=80)
    charges = models.IntegerField()


class NubankItem2(models.Model):

    created_at = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(max_digits=9, decimal_places=2)
    amount_without_iof = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=80)
    item_type = models.DateTimeField(verbose_name="time", help_text="2019-11-23T19:13:43Z")
    source = models.CharField(max_length=40)
    title = models.CharField(max_length=200)
    account = models.CharField(max_length=40)
    details = JSONField()
    nubank_id = models.CharField(max_length=40, verbose_name="id")
    href = models.CharField(max_length=200)

    index = models.IntegerField()
    charges = models.IntegerField()
