# Serializers

There are built-in serializers offered by the package.

## Table of Contents

---

- [Serializers](#serializers)
    - [Table of Contents](#table-of-contents)
    - [Notes](#notes)
    - [TenantSerializer](#tenantserializer)
    - [TenantListSerializer](#tenantlistserializer)
    - [CreateTenantSerializer](#createtenantserializer)
    - [TenantUserSerializer](#tenantuserserializer)

---

## Notes

The following serializers are used with the [views](./views.md) but can also
be used with any other custom view.

---

## TenantSerializer

Basic Tenant Serializer

- Renders:
    - `tenant_name` - String
    - `tenant_uuid` - String

Example:

```python
from django_tenants_url.serializers import TenantSerializer
from rest_framework.views import APIView
from django_tenants.utils import get_tenant_model


class MyView(APIView):
    serializer_class = TenantSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data or {}
        tenant_name = data.get("tenant_name")

        if tenant_name is None:
            raise ParseError(detail="tenant_name missing.")

        try:
            tenant = get_tenant_model().objects.get(tenant_name__iexact=tenant_name)
        except get_tenant_model().DoesNotExist:
            raise ParseError(detail=f"{tenant_name} does not exist.")

        serializer = self.serializer_class(tenant, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

## TenantListSerializer

Model serializer retrieving the information of the tenants.

- Renders:
    - `id` - Integer
    - `tenant_name` - String
    - `tenant_uuid` - String

Example:

```python
from django_tenants_url.serializers import TenantListSerializer
from rest_framework.generics import ListAPIView
from django_tenants.utils import get_tenant_model


class MyView(ListAPIView):
    serializer_class = TenantListSerializer
    queryset = get_tenant_model().objects.all()

```

## CreateTenantSerializer

For the creation of a tenant in the system.

- **Params**:
    - `tenant_name` - String (required).
    - `schema_name` - String (required).
    - `domain_url` - String (required).
    - `on_trial` - Boolean (optional, `default=False`).
    - `paid_until` - DateTime (optional, raises exception if `on_trial=True` and `paid_until=None`).
    - `is_primary` - Boolean (optional, `default=True`).

[Implementation example](./views.md#createtenantapiview).

## TenantUserSerializer

For the creation of a tenant user association.

- **Params**:
    - `user_id` - Integer (required).
    - `tenant_id` - Integer (required).
    - `is_active` - Boolean (required).

[Implementation example](./views.md#tenantuserapiview).
