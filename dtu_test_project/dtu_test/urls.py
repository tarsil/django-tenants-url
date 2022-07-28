"""dtu_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from dtu_test_app.views import ProductListAPIView, ProductTenantListAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("django-tenants-url/", include("django_tenants_url.urls")),
    # TEST ENDPOINTS
    path("product/list", ProductListAPIView.as_view(), name="product-list"),
    path(
        "product-tenant/list",
        ProductTenantListAPIView.as_view(),
        name="product-tenant-list",
    ),
]
