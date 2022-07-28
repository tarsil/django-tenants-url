# Permissions

Handling access permissions with `django-tenants-url` is like
doing using Django Rest Framework.

Django Tenants URL splits the middleware only used to map the UUID
of a tenant and route the connection and the permissions to access
a given tenant by validating the UUID of the header.

## Table of Contents

---

- [Permissions](#permissions)
    - [Table of Contents](#table-of-contents)
    - [BaseTenantPermission](#basetenantpermission)
    - [IsTenantAllowedOrPublic](#istenantallowedorpublic)

---

## BaseTenantPermission

The base used for the permissions of the tenants.

## IsTenantAllowedOrPublic

Checks if the user is allowed to access a specific tenant.
If no header is passed, it will return `True` defaulting to public.

When a header (default `X_REQUEST_ID`) is passed then checks if the
user has permission to access it, in other words, checks if there
is a tenant user (`TenantUserMixin`) associated.

Example:

```python
# views.py

from django_tenants_url.permissions import IsTenantAllowedOrPublic
from rest_framwork.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from myapp.models import Customer


class MyView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTenantAllowedOrPublic]

    def get(self, request, *args, **kwargs):
        return Customer.objects.all()

```
