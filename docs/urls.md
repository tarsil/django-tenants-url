# URLS

## Table of Contents

---

- [URLS](#urls)
    - [Table of Contents](#table-of-contents)
    - [How to import](#how-to-import)
    - [Available URLS](#available-urls)

---

## How to import

```python
# urls.py
from django.urls import include

...

urlpatterns = [
    ...
    path('tenants', include('django_tenants_url.urls'))
    ...
]

```

## Available URLS

```python

urlpatterns = [
    path("info", TenantAPIView.as_view(), name="tenant-info"),
    path("tenant", CreateTenantAPIView.as_view(), name="create-tenant"),
    path(
        "tenant/delete/<int:pk>", DestroyTenantAPIView.as_view(), name="delete-tenant"
    ),
    path("tenants", TenantListAPIView.as_view(), name="tenant-list"),
    path("tenant/user", TenantUserAPIView.as_view(), name="create-tenant-user"),
    path(
        "tenant/user/<int:user_id>/<int:tenant_id>",
        DestroyTenantUserAPIView.as_view(),
        name="delete-tenant-user",
    ),
    path(
        "tenant/user/<int:tenant_id>/set-active",
        SetActiveTenantUserAPIView.as_view(),
        name="set-active-tenant",
    ),
]
```
