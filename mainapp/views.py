import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
            .filter(create_date_time__month=item["number"], create_date_time__year=year)
            .annotate(sum_score=Sum("debit"))
        )

        item["data"] = [[x["category__name"], x["sum_score"]] for x in result]

    return render(request, "mainapp/index.html", {"data": data, "year": year})
