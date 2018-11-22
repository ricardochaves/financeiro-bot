import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django_filters import rest_framework as f_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from mainapp.models import Records
from mainapp.serializers import RecordsSerializer


class RecordsFilter(f_filters.FilterSet):
    db_included_date_time = f_filters.DateFromToRangeFilter()
    create_date_time = f_filters.DateFromToRangeFilter()
    payment_date_time = f_filters.DateFromToRangeFilter()

    class Meta:
        model = Records
        fields = fields = (
            "db_included_date_time",
            "create_date_time",
            "payment_date_time",
            "debit",
            "credit",
            "category__name",
            "name__name",
            "type_entry__name",
            "category__id",
            "name__id",
            "type_entry__id",
            "id",
        )


class RecordsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Records to be viewed or edited.
    """

    queryset = Records.objects.all()
    serializer_class = RecordsSerializer
    filter_fields = (
        "db_included_date_time",
        "create_date_time",
        "payment_date_time",
        "debit",
        "credit",
        "category__name",
        "name__name",
        "type_entry__name",
        "category__id",
        "name__id",
        "type_entry__id",
        "id",
    )
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = RecordsFilter


@login_required
def index(request):

    data = [
        {"month": "Janeiro", "number": "01", "data": []},
        {"month": "Fevereiro", "number": "02", "data": []},
        {"month": "Março", "number": "03", "data": []},
        {"month": "Abril", "number": "04", "data": []},
        {"month": "Maio", "number": "05", "data": []},
        {"month": "Junho", "number": "06", "data": []},
        {"month": "Julho", "number": "07", "data": []},
        {"month": "Agosto", "number": "08", "data": []},
        {"month": "Setembro", "number": "09", "data": []},
        {"month": "Outubro", "number": "10", "data": []},
        {"month": "Novembro", "number": "11", "data": []},
        {"month": "Dezembro", "number": "12", "data": []},
    ]

    year = request.GET.get("y", 2018)

    for item in data:
        result = (
            Records.objects.values("category__name")
            .filter(payment_date_time__month=item["number"], payment_date_time__year=year)
            .annotate(sum_score=Sum("debit"))
        )

        item["data"] = [[x["category__name"], x["sum_score"] if x["sum_score"] else 0] for x in result]

    return render(request, "mainapp/index.html", {"data": data, "year": year})


@login_required
def isabele(request):

    data = [
        {"month": "Janeiro", "number": "01", "data": []},
        {"month": "Fevereiro", "number": "02", "data": []},
        {"month": "Março", "number": "03", "data": []},
        {"month": "Abril", "number": "04", "data": []},
        {"month": "Maio", "number": "05", "data": []},
        {"month": "Junho", "number": "06", "data": []},
        {"month": "Julho", "number": "07", "data": []},
        {"month": "Agosto", "number": "08", "data": []},
        {"month": "Setembro", "number": "09", "data": []},
        {"month": "Outubro", "number": "10", "data": []},
        {"month": "Novembro", "number": "11", "data": []},
        {"month": "Dezembro", "number": "12", "data": []},
    ]

    year = request.GET.get("y", 2018)

    for item in data:
        q = Q(payment_date_time__month=item["number"], payment_date_time__year=year, category__id=1, name__id=2)
        result_debit = Records.objects.values("payment_date_time__month").filter(q).annotate(sum_score=Sum("debit"))
        result_credit = Records.objects.values("payment_date_time__month").filter(q).annotate(sum_score=Sum("credit"))

        value_credit = 0
        for i in result_credit:
            value_credit += i["sum_score"] if i["sum_score"] else 0

        value_debit = 0
        for i in result_debit:
            value_debit += i["sum_score"] if i["sum_score"] else 0

        value_credit = value_credit if value_credit else 0
        value_debit = value_debit if value_debit else 0

        result_final = value_credit - value_debit

        item["data"] = [item["month"], value_credit, value_debit, result_final]

    return render(request, "mainapp/isabele.html", {"data": data, "year": year})


@login_required
def meta100(request):

    data = [
        {"month": "Janeiro", "number": "01", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Fevereiro", "number": "02", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Março", "number": "03", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Abril", "number": "04", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Maio", "number": "05", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Junho", "number": "06", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Julho", "number": "07", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Agosto", "number": "08", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Setembro", "number": "09", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Outubro", "number": "10", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Novembro", "number": "11", "data": [], "totalcredit": 0, "totaldebit": 0},
        {"month": "Dezembro", "number": "12", "data": [], "totalcredit": 0, "totaldebit": 0},
    ]

    year = request.GET.get("y", 2018)

    for item in data:

        result = (
            Records.objects.annotate(month=TruncMonth("create_date_time"))
            .annotate(day=TruncDay("create_date_time"))
            .values("day")
            .filter(create_date_time__year=year, create_date_time__month=item["number"], type_entry__id=1)
            .annotate(sumdebit=Sum("debit"))
            .annotate(sumcredit=Sum("credit"))
            .order_by()
        )

        for r in result:
            sumcredit = r["sumcredit"] if r["sumcredit"] else 0
            sumdebit = r["sumdebit"] if r["sumdebit"] else 0

            item["data"].append(
                {
                    "day": r["day"].strftime("%d"),
                    "sumdebit": sumdebit,
                    "sumcredit": sumcredit,
                    "final": sumcredit - sumdebit,
                }
            )

            item["totalcredit"] += sumcredit
            item["totaldebit"] += sumdebit

    return render(request, "mainapp/meta100.html", {"data": data})
