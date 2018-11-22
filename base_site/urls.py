"""base_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

from mainapp import views

router = routers.DefaultRouter()
router.register(r"records", views.RecordsViewSet)
schema_view = get_schema_view(title="Records API")
swagger_view = get_swagger_view(title="Records API")

urlpatterns = (
    [
        url(r"api/v1/", include(router.urls)),
        path("api/v1/schema/", schema_view),
        path("api/v1/swagger/", swagger_view),
        path("ricardo/", admin.site.urls),
        url(r"^api/v1/api-auth/", include("rest_framework.urls")),
        path(r"api/v1/api-token-auth/", obtain_jwt_token),
        path(r"api/v1/api-token-refresh/", refresh_jwt_token),
        path("", views.index, name="index"),
        path("isabele", views.isabele, name="isabele"),
        path("meta100", views.meta100, name="meta100"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
