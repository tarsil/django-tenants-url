# Django Tenants URL

![Build and Publish](https://github.com/tarsil/django-tenants-url/actions/workflows/main.yml/badge.svg)

**Official Documentation** - <https://tarsil.github.io/django-tenants-url/>

---

## Table of Contents

- [Django Tenants URL](#django-tenants-url)
   - [Table of Contents](#table-of-contents)
   - [About Django Tenants URL](#about-django-tenants-url)
   - [Dependencies](#dependencies)
   - [Motivation](#motivation)
      - [Overview](#overview)
         - [Supported Django and Python Versions](#supported-django-and-python-versions)
   - [Installation](#installation)
      - [After installing django-tenants](#after-installing-django-tenants)
         - [Install django-tenants-url](#install-django-tenants-url)
      - [Django Tenants URL Settings](#django-tenants-url-settings)
      - [X_REQUEST_ID](#x_request_id)
   - [Example](#example)
   - [Documentation and Support](#documentation-and-support)
   - [License](#license)

---

## About Django Tenants URL

Django Tenants URL is a wrapper on the top of the `django-tenants` package that serves a different
yet common use case, the multi-tenant implementation via HEADER and not using `sub domains`.

A special thanks to the team behind [Django Tenants](https://github.com/django-tenants/django-tenants).

## Dependencies

The project contains [views](./views.md), [permissions](./permissions.md),
[models](./models.md) and more addons that can be used across projects.

`django-tenants-url` is built on the top of the following dependencies:

1. [Django](https://www.djangoproject.com/)
2. [Django Rest Framework](https://www.django-rest-framework.org/)
3. [Django Tenants](https://django-tenants.readthedocs.io/en/latest/)

## Motivation

When implementing multi tenancy architecture there are many factors to consider and cover and
those were greatly approached by [django-tenants](https://github.com/django-tenants/django-tenants)
but so summarize, there are 3 common ways:

1. **Shared schemas** - The data of all users are shared within the same schema and filtered by
   common IDs or whatever that is unique to the platform. This is not so great for GDPR.
2. **Shared database, different Schemas** - The user's data is split by different schemas but live
   on the same database.
3. **Different databases** - The user's data or any data live on different databases.

As mentioned before, `django-tenants-url` is a wrapper on the top of `django-tenants`
and therefore we will be approaching the second.

Many companies have limited resources (money, people...) and limited choices from those
constraints. When implementing multi tenancy, the default would be to use subdomains
in order to access the desired schema. E.g.:

```shell
www.mycompany.saascompany.com
```

`My Company` is the tenant of the `saascompany.com` that is publicaly available to the users.
When the `mycompany` is sent to the backend, the middleware splits the subdomain and
the TLD (top-level domain) and maps the tenant with the schema associated.

For this work, one of the ways is to change your `apache`, `nginx` or any other configurations
that accepts and forwards calls to the `*.sasscompany.com` and performs the above action.

If the frontend and backend are split, extra configurations need also to be made on that
front and all of this can be a pain.

**What does django-tenants-url solve?**

The principle of mapping users to the schemas remains the same but the way of doing it
is what diverges from the rest. What if we were able to only use `www.sasscompany.com`,
login as usual and automatically the platform knows exactly to which schema the user
needs to be mapped and forward?

**This is what django-tenants-url solves. A single url that does the multi tenancy
without breaking the principle and architecture and simply using one single url**

### Overview

#### Supported Django and Python Versions

| Django / Python | 3.7 | 3.8 | 3.9 | 3.10 |
| --------------- | --- | --- | --- | ---- |
| 2.2             | Yes | Yes | Yes | Yes  |
| 3.0             | Yes | Yes | Yes | Yes  |
| 3.1             | Yes | Yes | Yes | Yes  |
| 3.2             | Yes | Yes | Yes | Yes  |
| 4.0             | Yes | Yes | Yes | Yes  |

## Installation

Prior to install the `django-tenants-url`, `django-tenants` needs to be installed
as well. Please follow the installation steps from
[Django Tenants](https://www.github.com/django-tenants/django-tenants)

### After installing django-tenants

#### Install django-tenants-url

```shell
pip install django-tenants-url
```

1. The `TENANT_MODEL` and `TENANT_DOMAIN_MODEL` from `django-tenants`
   need to be also in the `settings.py`.
2. Add `django-tenants-url` to `INSTALLED_APPS`.

   ```python

   INSTALLED_APPS = [
     ...
     'django_tenants',
     'django_tenants_url',
     ...
   ]

   ```

3. `django-tenants-url` offers a special wrapper over the `mixins` of `django-tenants`
   with the same names so you don't need to worry about breaking changes and the
   additional unique `TenantUserMixin` that maps the users with a tenant.

4. Create the models.

   ```python
   # myapp.models.py

   from django.db import models
   from django_tenants_url.models import TenantMixin, DomainMixin, TenantUserMixin


   class Client(TenantMixin):
       """
       This table provides the `tenant_uuid` needed
       to be used in the `X_REQUEST_HEADER` and consumed
       by the RequestUUIDTenantMiddleware.
       """
       pass


   class Domain(DomainMixin):
       pass


   class TenantUser(TenantUserMixin):
       pass

   ```

5. Add the `DTU_TENANT_USER_MODEL` to `settings.py`.

   ```python
   # settings.py

   ...

   DTU_TENANT_USER_MODEL = 'myapp.TenantUser'

   ...

   ```

6. Update the `MIDDLEWARE` to have the new `RequestUUIDTenantMiddleware`.
   Preferentially at the very top.

   ```python
   # settings.py

   ...

   MIDDLEWARE = [
     'django_tenants_url.middleware.RequestUUIDTenantMiddleware',
     'django.middleware.security.SecurityMiddleware',
     ...
   ]

   ...
   ```

7. Generate the migrations.

   ```shell
   python manage.py makemigrations
   ```

8. Run the migrations as if it was `django-tenants` and not the classic `migrate`.

   ```shell
   python manage.py migrate_schemas
   ```

9. The `UUID` needed for the `RequestUUIDTenantMiddleware` can be found in your
   table inherited from the `TenantMixin`.

**None: Do not run `python manage.py migrate` or else it will sync everything into the public.**

And that is it. The `RequestUUIDTenantMiddleware` should be able to map
the `TenantUser` created with a tenant and route the queries to the associated schema.

Checkout the [documentation](https://tarsil.github.io/django-tenants-url/)
and understand how to integrate with your views and taking advantage
of the utils for your `TenantUser` (or your implementation),

### Django Tenants URL Settings

```python
# default settings

DTU_TENANT_NAME = "Public"
DTU_TENANT_SCHEMA = "public"
DTU_DOMAIN_NAME = "localhost"
DTU_PAID_UNTIL = "2100-12-31"
DTU_ON_TRIAL = False
DTU_HEADER_NAME = "HTTP_X_REQUEST_ID"
DTU_AUTO_CREATE_SCHEMA = True
DTU_AUTO_DROP_SCHEMA = False
DTU_TENANT_USER_MODEL = None

```

### X_REQUEST_ID

By default `django-tenants-url` has the header name `HTTP_X_REQUEST_ID` that will be lookup
from the middleware when sent via HTTP.
This name can be overriten by the special setting `DTU_HEADER_NAME`.

## Example

A Django Like app implementing Django Tenants Url can be found [here](https://github.com/tarsil/django-tenants-url/tree/main/dtu_test_project).

The example can be found [here](./example.md)

## Documentation and Support

Full documentation for the project is available at <https://tarsil.github.io/django-tenants-url/>

## License

Copyright (c) 2022-present Tiago Silva and contributors under the [MIT license](https://opensource.org/licenses/MIT).
