# Handlers

`djang-tenants-url` offers some handlers that facilitates the creation or update
or creation of new domain, tenants and tenant users

## Table of Contents

---

- [Handlers](#handlers)
    - [Table of Contents](#table-of-contents)
    - [handle_tenant](#handle_tenant)
    - [handle_domain](#handle_domain)
    - [handle_tenant_user](#handle_tenant_user)

---

## handle_tenant

Creates a tenant and a schema for the same tenant. E.g.:

```python

from django_tenants_url.handlers import handle_tenant

tenant = handle_tenant(
    domain_url='myexample.com', tenant_name='mytenant', schema_name='myschema'
)


```

## handle_domain

Creates a domain for a given tenant. E.g.:

```python

from django_tenants_url.handlers import handle_domain, handle_tenant

tenant = handle_tenant(
    domain_url='myexample.com', tenant_name='mytenant', schema_name='myschema'
)

domain = handle_domain(
    domain_url='myexample.com', tenant=tenant, is_primary=True
)

```

## handle_tenant_user

Creates a tenant user relation. E.g.:

```python

from django_tenants_url.handlers import handle_tenant, handle_tenant_user
from django.contrib.auth import get_user_model

user = get_user_model().objects.get(email='foobar@example.com')

tenant = handle_tenant(
    domain_url='myexample.com', tenant_name='mytenant', schema_name='myschema'
)

# if is_active=True, that only facilitates which tenant is currently active
# for the user. This can help filter schemas on logins, for example.
tenant_user = handle_tenant_user(
    tenant=tenant, user=user, is_active=True
)


```
