# Example

---

Here follows an example in how to use `django-tenants-url`.

## Table of Contents

- [Example](#example)
    - [Table of Contents](#table-of-contents)
    - [Initial Notes](#initial-notes)
    - [Install package](#install-package)
    - [Settings](#settings)
    - [Create Tenant django app](#create-tenant-django-app)
    - [Create and run migrations](#create-and-run-migrations)
    - [Update settings](#update-settings)
    - [Start the server](#start-the-server)
    - [Get a Tenant UUID](#get-a-tenant-uuid)
    - [Use the UUID within the headers](#use-the-uuid-within-the-headers)

---

## Initial Notes

This is a very basic example how to see the UUID of a tenant and use it in the headers.
For more robust and secure approach we also provide [views](./views.md),
[serializers](./serializers.md), [utils](./utils.md) and some [permissions](./permissions.md)
and [handlers](./handlers.md) that can be used accordingly.

## Install package

```shell
pip install django-tenants-url
```

## Settings

After installing `django-tenants-url`, add it into the settings.

```python

INSTALLED_APPS = [
    ...
    'django_tenants',
    'django_tenants_url',
    ...
]
```

## Create Tenant django app

Let's create a tenant custom app and add it into the settings.

1. Create the app

   ```shell
   django-admin startapp tenant
   ```

2. Add the app to the `INSTALLED_APPS`.

3. ```python
   INSTALLED_APPS = [
       ...
       'django_tenants',
       'django_tenants_url',
       'tenant',
       ...
   ]
   ```

More settings will be needed but we will back later on to update the settings.

## Create the models

1. Inside the newly created `tenant` in the `models.py`.

   ```python
   from django_tenants_url.models import TenantMixin, DomainMixin, TenantUserMixin


   class Client(TenantMixin):
       pass


   class Domain(DomainMixin):
       pass


   class TenantUser(TenantUserMixin):
       pass

   ```

## Create and run migrations

1. Create migrations.

   ```shell
   python manage.py makemigrations
   ```

2. Run migrations.

   ```shell
   python manage.py migrate_schemas
   ```

## Update settings

With the models created we can now update the `settings.py`.

1. Add extra needed settings.

   ```python

   INSTALLED_APPS = [...]

   TENANT_MODEL = 'tenant.Client' # needed from django-tenants

   TENANT_DOMAIN_MODEL = 'tenant.Domain' # needed from django-tenants

   # DTU_TENANT_USER_MODEL
   DTU_TENANT_USER_MODEL = 'tenant.TenantUser' # unique to django-tenants-url

   ```

2. Update the `MIDDLEWARE`.

   ```python
   MIDDLEWARE = [
       'django_tenants_url.middleware.RequestUUIDTenantMiddleware',
       'django.middleware.security.SecurityMiddleware',
       ...
   ]
   ```

## Start the server

Once the first request hits the server, it should create the public tenant and public domain.

## Get a Tenant UUID

`django-tenants-url` provides out-of-the-box [views](./views.md) to help you with all of the process as well
as some functions that can be used to get some of the information like the UUID needed
to be used in the header of a request and map to user schema.

```python
from django_tenants_url.utils import get_tenants

tenants = get_tenants()
print(tenants)

[
    {
        "id": 1,
        "tenant_name": "Public",
        "tenant_uuid": "a66b19e4-3985-42a1-87e1-338707c4a203"
    }
]

```

## Use the UUID within the headers

Using the uuid `a66b19e4-3985-42a1-87e1-338707c4a203` we can now use the header
that maps the user with the schema.

```cURL
curl --header "X_REQUEST_ID: a66b19e4-3985-42a1-87e1-338707c4a203" -v http://localhost:8000/my-view
```
