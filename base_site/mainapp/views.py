from base_site.mainapp.models import Category
from django.shortcuts import render


def index(request):
    categorys = Category.objects.all()

    return render(request, "mainapp/index.html", {"categorys": categorys})
