from datetime import datetime

from django.db import models


class TypeEntry(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nome", default="", blank=False, null=False)

    def __str__(self):
        return self.name


class FamilyMember(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nome", default="", blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nome", default="", blank=False, null=False)
    enable = models.BooleanField(default=True, verbose_name="Enable?")

    def __str__(self):
        return self.name


class FullCommand(models.Model):

    PAYMENT_DATE_OPTIONS = (
        (1, "Data do Dia"),
        (2, "Data do Cartão (15)"),
        (3, "Perguntar"),
        (4, "Dia Seguinte"),
        (5, "Mês Seguinte"),
        (6, "Dia 5 mês vigente"),
        (7, "Dia 5 mês que vem"),
        (8, "Crédito Parcelado"),
    )

    command = models.CharField(max_length=70, verbose_name="Comando", default="", blank=False, null=False)
    entry_date = models.BooleanField(verbose_name="Data de Lançamento: Usa data do dia?")
    payment_date = models.IntegerField(choices=PAYMENT_DATE_OPTIONS, verbose_name="Data de Pagamento", default=1)
    debit = models.DecimalField(max_digits=6, verbose_name="Débito", decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=6, verbose_name="Crédito", decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria", blank=True, null=True)
    name = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, blank=True, verbose_name="Nome", null=True)
    description = models.CharField(max_length=400, verbose_name="Descrição", blank=True, null=True)
    type_entry = models.ForeignKey(TypeEntry, on_delete=models.CASCADE, verbose_name="Tipo", blank=True, null=True)

    def __str__(self):
        return self.command


class Records(models.Model):

    db_included_date_time = models.DateTimeField(auto_now=True, null=False, verbose_name="Inclusão no Bando de Dados")
    create_date_time = models.DateTimeField(
        default=datetime.now, null=False, blank=False, verbose_name="Data do Lançamento"
    )
    payment_date_time = models.DateTimeField(
        default=datetime.now, null=True, blank=False, verbose_name="Data da Execução"
    )

    debit = models.DecimalField(max_digits=6, verbose_name="Débito", decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=6, verbose_name="Crédito", decimal_places=2, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria", blank=True, null=True)
    name = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, blank=True, verbose_name="Nome", null=True)
    type_entry = models.ForeignKey(TypeEntry, on_delete=models.CASCADE, verbose_name="Tipo", blank=True, null=True)

    description = models.CharField(max_length=400, verbose_name="Descrição", default="", blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["db_included_date_time"], name="db_included_date_time_idx"),
            models.Index(fields=["create_date_time"], name="create_date_time_idx"),
            models.Index(fields=["payment_date_time"], name="payment_date_time_idx"),
            models.Index(fields=["category"], name="category_idx"),
            models.Index(fields=["name"], name="name_idx"),
            models.Index(fields=["type_entry"], name="type_entry_idx"),
        ]


class Goal(models.Model):

    PERIOD_CHOICES = ((1, "This Week"),)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria", blank=True, null=True)
    name_family = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, blank=True, verbose_name="Nome", null=True)
    type_entry = models.ForeignKey(TypeEntry, on_delete=models.CASCADE, verbose_name="Tipo", blank=True, null=True)
    name = models.CharField(max_length=40, verbose_name="Name")
    value = models.DecimalField(max_digits=6, verbose_name="Value", decimal_places=2)

    period = models.IntegerField(choices=PERIOD_CHOICES, verbose_name="Data de Pagamento", default=1)

    enable = models.BooleanField(default=True, verbose_name="Enable")

    def __str__(self):
        return self.name
