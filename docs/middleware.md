# Middleware

The core of `django-tenants-url` is the custom `MIDDLEWARE`.

## Table of Contents

---

- [Middleware](#middleware)
   - [Table of Contents](#table-of-contents)
   - [Installation](#installation)

---

## Installation

1. Add the `TENANT_USER_MODEL` to `settings.py`.

   ```python
   # settings.py

   ...

   DTU_TENANT_USER_MODEL = 'myapp.TenantUser'

   ...

   ```

2. Update the `MIDDLEWARE` to have the new `RequestUUIDTenantMiddleware`.
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
