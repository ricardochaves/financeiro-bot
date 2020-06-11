from django.db import models


class Broker(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=300)
    paper = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.paper


class BrokersNote(models.Model):
    date = models.DateField()
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    number = models.CharField(max_length=30)
    link = models.URLField()
    brokerage_fee = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    settlement_fee = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    Emonuments_fee = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    irrf = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    final_value = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")

    class Meta:
        unique_together = [["broker", "number"]]


class BrokersNoteItem(models.Model):
    note = models.ForeignKey(BrokersNote, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    unit = models.IntegerField()
    buy_or_sell = models.CharField(max_length=1)
    credit_or_debit = models.CharField(max_length=1)
    value = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.company.paper
