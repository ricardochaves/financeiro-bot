import logging

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


def index(request):

    month = request.GET.get("q", 11)

    r = Records.objects.values("category__name").filter(create_date_time__month=month).annotate(sum_score=Sum("debit"))

    result = [[x["category__name"], x["sum_score"]] for x in r]

    return render(request, "mainapp/index.html", {"data": result})
