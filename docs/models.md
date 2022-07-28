# Models

`django-tenants` offers a set of models that can and should be use to facilitate
the integration of multi-tenancy.

`django-tenants-url` wraps those same models and adds some extra flavours to make
sure it serves the purpose of a unified url for all tenants.

---

## Table of Contents

- [Models](#models)
  - [Table of Contents](#table-of-contents)
  - [TenantMixin](#tenantmixin)
  - [DomainMixin](#domainmixin)
  - [TenantUserMixin](#tenantusermixin)
  - [Handlers](#handlers)

---

## TenantMixin

1. `TenantMixin` is where the tenant information is stored.

   ```python
   from django_tenants_url.models import TenantMixin


   class Tenant(TenantMixin):
        # Customize, override or leave it be
        pass

   ```

## DomainMixin

1. `DomainMixin` is where the domain of a tenant is stored.

   ```python
   from django_tenants_url.models import DomainMixin


   class Domain(DomainMixin):
        # Customize, override or leave it be
        pass

   ```

## TenantUserMixin

1. `TenantUserMixin` is where the mapping between a tenant and a user of the system
   is stored. This is one of the main differences that diverges from `django-tenants` and
   what allows the integration of a unified URL for all users and tenants in the system.

   ```python
   from django_tenants_url.models import TenantUserMixin


   class TenantUser(TenantUserMixin):
        # Customize, override or leave it be
        pass

   ```

## Handlers

To help with the process of the creation of a domain and tenant we can
also use `handle_domain` and `handle_tenant`. [More on this here](./handlers.md).
