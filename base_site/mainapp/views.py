from base_site.mainapp.models import Category
from base_site.mainapp.models import Records
from base_site.mainapp.serializers import RecordsSerializer
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django_filters import rest_framework as f_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets


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
    categorys = Category.objects.all()

    return render(request, "mainapp/index.html", {"categorys": categorys})


@login_required
def variableyear(request):

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
            .filter(payment_date_time__month=item["number"], payment_date_time__year=year, type_entry__id=1)
            .annotate(sum_score=Sum("debit"))
        )

        item["data"] = [[x["category__name"], x["sum_score"] if x["sum_score"] else 0] for x in result]

    return render(request, "mainapp/variableyear.html", {"data": data, "year": year})


@login_required
def bycategory(request):

    data = []
    category = None

    year = request.GET.get("y", 2018)
    categoryid = request.GET.get("c", 1)

    result = (
        Records.objects.annotate(month=TruncMonth("create_date_time"))
        .values("month", "category")
        .filter(create_date_time__year=year, category_id=categoryid)
        .annotate(sumdebit=Sum("debit"))
        .annotate(sumcredit=Sum("credit"))
        .order_by()
    )

    for item in result:

        sumcredit = item["sumcredit"] if item["sumcredit"] else 0
        sumdebit = item["sumdebit"] if item["sumdebit"] else 0

        data.append([item["month"], sumdebit, sumcredit, sumcredit - sumdebit])

        category = Category.objects.get(pk=item["category"])

    return render(request, "mainapp/bycategory.html", {"data": data, "category": category})
