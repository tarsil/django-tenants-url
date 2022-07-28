# Views

Using multi tenancy can be complicated sometimes and the initial
configurations can take some time to get around.

`django-tenants-url` has some built-in views to help with the process
but those can be replaced by any custom view.

The views are built on the top of [Django Rest Framework](https://www.django-rest-framework.org/).

## Table of Contents

---

- [Views](#views)
    - [Table of Contents](#table-of-contents)
    - [Initial Notes](#initial-notes)
    - [Inherited Views](#inherited-views)
    - [Import Views](#import-views)
    - [Import URLs](#import-urls)
    - [TenantListAPIView](#tenantlistapiview)
    - [TenantAPIView](#tenantapiview)
    - [CreateTenantAPIView](#createtenantapiview)
    - [DestroyTenantAPIView](#destroytenantapiview)
    - [TenantUserAPIView](#tenantuserapiview)
    - [DestroyTenantUserAPIView](#destroytenantuserapiview)
    - [SetActiveTenantUserAPIView](#setactivetenantuserapiview)

---

## Initial Notes

The views below are built-in from the `django-tenants-url` and those can be used directly:

- [Per Mixin](#inherited-views)
- [Per import](#import-views)
- [Per URL](#import-urls)

The [urls](./urls.md) can also be imported and used directly.

## Inherited Views

One way to use the views is by simply inheriting to be used with any system and permissions.

Example:

```python
# views.py

...
from django_tenants_url.views import CreateTenantAPIView
...


class MyCustomView(MyCustomAuthMixin, CreateTenantAPIView):
    permission_classes = [IsAuthenticated, MyCustomTenantPermission]

    ...

```

## Import Views

To import all the built-in views from the project, simply use the standard imports.

Example.:

```python
from django_tenants_url.views import (
    CreateTenantAPIView,
    DestroyTenantAPIView,
    DestroyTenantUserAPIView,
    SetActiveTenantUserAPIView,
    TenantAPIView,
    TenantListAPIView,
    TenantUserAPIView
)

...
```

## Import URLs

The views can be directly imported into a project via normal django url imports.

Example:

```python
# urls.py

from django.urls import include

urlpatterns = [
    ...
    path('tenants', include('django_tenants_url.urls')),
    ...
]

```

---

## TenantListAPIView

Lists all the tenants in the system. No params required.

- Method: `GET`.

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview

response = requests.get(url)

```

## TenantAPIView

Returns the information of a given tenant.

- Method: `POST`.
- **Params**:
    - `tenant_name` - String (required)

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview
params = {
    'tenant_name': 'Public'
}

response = requests.post(url, params=params)

```

## CreateTenantAPIView

Creates a tenant and corresponding schema in the system.

- Method: `POST`.
- **Params**:
    - `tenant_name` - String (required).
    - `schema_name` - String (required).
    - `domain_url` - String (required).

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview
params = {
    'tenant_name': 'My Company',
    'schema_name': 'my_company',
    'domain_url': 'mycompany.com'
}

response = requests.post(url, params=params)

```

## DestroyTenantAPIView

Removes a tenant and domains associated to the tenant from the system.

- Method: `DELETE`.
- **Params**:
    - `id` - Integer (URL parameter, required).

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview/2

response = requests.delete(url)

```

## TenantUserAPIView

Associates a system user with a system tenant and sets to active.

- Method: `POST`.
- **Params**:
    - `user_id` - Integer (URL parameter, required).
    - `tenant_id` - Integer (URL parameter, required).
    - `is_active` - Boolean (URL parameter, required).

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview
params = {
    'user_id': 12,
    'tenant_id': 25,
    'is_active': True
}

response = requests.post(url, params=params)

```

## DestroyTenantUserAPIView

Removes the association of a system user and a tenant.

- Method: `DELETE`.
- **Params**:
    - `user_id` - Integer (URL parameter, required).
    - `tenant_id` - Integer (URL parameter, required).

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview/12/25

response = requests.delete(url)

```

## SetActiveTenantUserAPIView

Sets the current active tenant of a request user (logged in).

- Method: `PUT`.
- **Params**:
    - `tenant_id` - Integer (URL parameter, required).

Example:

```python
import requests

url = 'http://localhost:8000/api/v1/myview/25

response = requests.put(url)

```
